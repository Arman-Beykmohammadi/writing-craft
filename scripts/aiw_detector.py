#!/usr/bin/env python3
"""Deterministic AI-writing detector: a Python port of avoid-ai-writing.

Ports detector/patterns.js (analyzeText) and the bin/avoid-ai-writing.js CLI
from avoid-ai-writing v3.36.0 (https://github.com/conorbronsdon/avoid-ai-writing),
MIT License, Copyright (c) 2026 Conor Bronsdon. The verbatim JavaScript lives
in upstream/; tests/parity/run_parity.py checks this port against it.

The output matches the JavaScript result exactly: the same keys in the same
order, the same issue order, score, label, classification, probabilities and
highlight regions. Offsets (issue index, region start/end) count UTF-16 code
units, as JavaScript does, so an emoji counts as 2.

Library use:
    from aiw_detector import analyze_text
    result = analyze_text(text, 'general', 'plain')

CLI:
    python3 aiw_detector.py [--context general|technical|marketing|personal]
                            [--source-mode plain|rendered-markdown] [file|-]

Standard library only; Python 3.9 compatible.
"""

import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiw_jscompat import (  # noqa: E402
    JS_WS_CHARS, LT, NOT_WS, UNDEFINED, WS, exec_all, from_u16, js_lower, js_re,
    js_round, js_stringify, js_to_fixed, js_trim, js_trim_end, js_trim_start, js_truthy,
    node_fs_error, py_re, to_u16, write_stderr, write_stdout,
)

# ─── Rule tables (regex sources copied verbatim from patterns.js) ──────────

CYRILLIC_LOOKALIKES = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'х': 'x',
    'у': 'y', 'к': 'k', 'м': 'm', 'н': 'h', 'в': 'b', 'т': 't',
    'А': 'A', 'Е': 'E', 'О': 'O', 'Р': 'P', 'С': 'C', 'Х': 'X',
    'У': 'Y', 'К': 'K', 'М': 'M', 'Н': 'H', 'В': 'B', 'Т': 'T',
}
GREEK_LOOKALIKES = {'ο': 'o', 'Ο': 'O', 'α': 'a', 'Α': 'A', 'ρ': 'p', 'Ρ': 'P'}
ZERO_WIDTH = frozenset('​‌‍﻿⁠')

TIER1 = {
    'delve': 'explore, dig into, look at',
    'tapestry': 'describe the actual complexity',
    'paradigm': 'model, approach, framework',
    'beacon': 'rewrite entirely',
    'robust': 'strong, reliable, solid',
    'comprehensive': 'thorough, complete, full',
    'cutting-edge': 'latest, newest, advanced',
    'pivotal': 'important, key, critical',
    'meticulous': 'careful, detailed, precise',
    'meticulously': 'carefully, precisely',
    'seamless': 'smooth, easy, without friction',
    'seamlessly': 'smoothly, easily',
    'game-changer': 'describe what changed',
    'game-changing': 'describe what changed',
    'nestled': 'is located, sits',
    'vibrant': 'describe what makes it active',
    'thriving': 'growing, active',
    'bustling': 'busy, active',
    'intricate': 'complex, detailed',
    'intricacies': 'complexities, details',
    'ever-evolving': 'changing, growing',
    'enduring': 'lasting, long-running',
    'daunting': 'hard, difficult',
    'holistic': 'complete, full, whole',
    'holistically': 'completely, fully',
    'actionable': 'practical, useful, concrete',
    'impactful': 'effective, significant',
    'learnings': 'lessons, findings, takeaways',
    'synergy': 'describe the combined effect',
    'synergies': 'describe the combined effect',
    'interplay': 'relationship, connection',
    'symphony': 'describe the coordination',
    'embrace': 'adopt, accept, use',
}

TIER1_PHRASES = [
    ((r'\bdelve\s+into\b', 'gi'), 'explore, dig into', False),
    ((r'\blandscape\b', 'gi'), 'field, space, industry', False),
    ((r'\brealm\b', 'gi'), 'area, field, domain', False),
    ((r'\btestament\s+to\b', 'gi'), 'shows, proves', False),
    ((r'\bleverag(?:e|es|ing|ed)\b', 'gi'), 'use', False),
    ((r'\bwatershed\s+moment\b', 'gi'), 'turning point, shift', False),
    ((r'\bmarking\s+a\s+pivotal\s+moment\b', 'gi'), 'state what happened', False),
    ((r'\bthe\s+future\s+looks\s+bright\b', 'gi'), 'cut or say something specific', False),
    ((r'\bonly\s+time\s+will\s+tell\b', 'gi'), 'cut or say something specific', False),
    ((r'\bdespite\s+challenges[^.]*continues?\s+to\s+thrive\b', 'gi'), 'name the challenge and response', False),
    ((r'\bdeep\s+dive\b', 'gi'), 'look at, examine', False),
    ((r'\bdive\s+into\b', 'gi'), 'look at, examine', False),
    ((r'\bunpack(?:ing)?\b', 'gi'), 'explain, break down', False),
    ((r'\bcomplexities\b', 'gi'), 'name the actual problems', False),
    ((r'\bthought\s+leader(?:ship)?\b', 'gi'), 'expert, authority', False),
    ((r'\bbest\s+practices\b', 'gi'), 'what works, proven methods', False),
    ((r'\bat\s+its\s+core\b', 'gi'), 'cut, just state it', False),
    ((r'\bin\s+order\s+to\b', 'gi'), 'to', True),
    ((r'\bdue\s+to\s+the\s+fact\s+that\b', 'gi'), 'because', True),
    ((r'\bserves\s+as\b', 'gi'), 'is', True),
    ((r'\bfeatures\b', 'gi'), 'has, includes', True),
    ((r'\bboasts\b', 'gi'), 'has', True),
    ((r'\butiliz(?:e|es|ing|ed)\b', 'gi'), 'use', True),
    ((r'\bshowcas(?:e|es|ing|ed)\b', 'gi'), 'show, demonstrate', False),
    ((r'\bembark(?:s|ing|ed)?\b', 'gi'), 'start, begin', False),
    ((r'\bcommenc(?:e|es|ing|ed)\b', 'gi'), 'start, begin', True),
    ((r'\bascertain(?:s|ing|ed)?\b', 'gi'), 'find out, determine', True),
    ((r'\bendeavou?r(?:s|ing|ed)?\b', 'gi'), 'effort, attempt, try', True),
    ((r'\bunderscor(?:es|ing|ed)\b', 'gi'), 'highlights, shows', False),
    ((r'\bload-bearing\b(?=[ \t]+(?:assumptions?|claims?|invariants?|premises?|constraints?|dependenc(?:y|ies)|arguments?|abstractions?)\b)', 'gi'), 'essential, critical, or say what breaks if you remove it', False),
]

TIER2 = {
    'harness': 'use, take advantage of',
    'navigate': 'work through, handle',
    'navigating': 'working through, handling',
    'foster': 'encourage, support, build',
    'elevate': 'improve, raise, strengthen',
    'unleash': 'release, enable, unlock',
    'streamline': 'simplify, speed up',
    'empower': 'enable, let, allow',
    'bolster': 'support, strengthen',
    'spearhead': 'lead, drive, run',
    'resonate': 'connect with, appeal to',
    'resonates': 'connects with, appeals to',
    'revolutionize': 'change, transform',
    'facilitate': 'enable, help, allow',
    'facilitates': 'enables, helps, allows',
    'underpin': 'support, form the basis of',
    'nuanced': 'specific, subtle, detailed',
    'crucial': 'important, key, necessary',
    'multifaceted': 'describe the actual facets',
    'ecosystem': 'system, community, network',
    'myriad': 'many, numerous',
    'plethora': 'many, a lot of',
    'encompass': 'include, cover, span',
    'catalyze': 'start, trigger, accelerate',
    'reimagine': 'rethink, redesign, rebuild',
    'galvanize': 'motivate, rally, push',
    'augment': 'add to, expand, supplement',
    'cultivate': 'build, develop, grow',
    'illuminate': 'clarify, explain, show',
    'elucidate': 'explain, clarify',
    'juxtapose': 'compare, contrast',
    'transformative': 'describe what changed',
    'transformation': 'describe what changed',
    'cornerstone': 'foundation, basis, key part',
    'paramount': 'most important, top priority',
    'poised': 'ready, set, about to',
    'burgeoning': 'growing, emerging',
    'nascent': 'new, early-stage',
    'quintessential': 'typical, classic, defining',
    'overarching': 'main, central, broad',
    'quietly': 'cut, or name the concrete contrast',
    'underpinning': 'basis, foundation',
    'underpinnings': 'basis, foundations',
    'paradigm-shifting': 'describe what shifted',
}

TIER2_CONDITIONAL = [
    ('deeply', (r'\bdeeply\s+(?:integrated|committed|rooted|personal|human|flawed|resonant|transformative|interconnected|ingrained|embedded|meaningful)\b', 'i'), 'cut, or name what specifically runs deep'),
]

TIER3 = [
    'significant',
    'significantly',
    'innovative',
    'innovation',
    'effective',
    'effectively',
    'dynamic',
    'dynamics',
    'scalable',
    'scalability',
    'compelling',
    'unprecedented',
    'exceptional',
    'exceptionally',
    'remarkable',
    'remarkably',
    'sophisticated',
    'instrumental',
    'world-class',
    'state-of-the-art',
    'best-in-class',
    'verbatim',
]

ISSUE_WEIGHTS = {
    'tier1': 5,
    'tier1-clarity': 3,
    'tier2': 3,
    'tier3': 2,
    'transition': 2,
    'chatbot': 8,
    'sycophantic': 8,
    'filler': 2,
    'generic-conclusion': 3,
    'lets-construction': 2,
    'reasoning-artifact': 6,
    'significance-inflation': 4,
    'vague-attribution': 5,
    'hollow-intensifier': 2,
    'emotional-flatline': 0,
    'lingering-attention': 3,
    'novelty-inflation': 3,
    'cutoff-disclaimer': 10,
    'template-phrase': 3,
    'false-concession': 2,
    'rhetorical-question': 2,
    'confidence-calibration': 2,
    'em-dash': 0,
    'uniformity': 5,
    'formatting': 3,
    'tier3-phrase': 3,
    'tier3-phrase-cluster': 12,
    'hashtag-stuff': 12,
    'bullet-np-list': 10,
    'hedge-stack': 6,
    'future-narrative': 12,
    'real-actual-inflation': 5,
    'social-cta-closer': 8,
    'performed-insight': 3,
    'negation-chain': 5,
    'dev-blog-boilerplate': 3,
    'formulaic-opener': 8,
    'speculative-opener': 8,
    'launch-intro': 8,
    'crowd-contrast': 6,
    'fake-casual-prop': 8,
    'title-case-header': 4,
    'parenthetical-hedge': 3,
    'smart-punct-signature': 6,
    'punct-distribution': 6,
    'fnword-trigram-entropy': 5,
    'cross-para-burstiness': 5,
    'normalization-flag': 9,
    'low-ttr': 3,
    'ai-placeholder': 10,
    'ai-citation-markup': 15,
    'ai-utm-source': 12,
    'unnecessary-hyphenation': 0,
}

TECHNICAL_EXEMPT = frozenset([
    'robust',
    'comprehensive',
    'seamless',
    'seamlessly',
    'ecosystem',
    'leverage',
    'leverages',
    'leveraging',
    'leveraged',
    'facilitate',
    'facilitates',
    'underpin',
    'underpinning',
    'underpinnings',
    'streamline',
])

TRANSITIONS = [
    (r'\bmoreover\b', 'gi'),
    (r'\bfurthermore\b', 'gi'),
    (r'\badditionally\b', 'gi'),
    (r"\bin\s+today'?s\b", 'gi'),
    (r'\bin\s+an\s+era\s+where\b', 'gi'),
    (r"\bit'?s\s+worth\s+noting\s+that\b", 'gi'),
    (r'\bnotably\b', 'gi'),
    (r'\bin\s+conclusion\b', 'gi'),
    (r'\bin\s+summary\b', 'gi'),
    (r'\bto\s+summarize\b', 'gi'),
    (r'\bwhen\s+it\s+comes\s+to\b', 'gi'),
    (r'\bat\s+the\s+end\s+of\s+the\s+day\b', 'gi'),
    (r'\bthat\s+(?:being\s+)?said\b', 'gi'),
]

CHATBOT_ARTIFACTS = [
    (r'\bi\s+hope\s+this\s+helps\b', 'gi'),
    (r'\bcertainly!\b', 'gi'),
    (r'\babsolutely!\b', 'gi'),
    (r'\bgreat\s+question!\b', 'gi'),
    (r'\bexcellent\s+point!\b', 'gi'),
    (r'\bfeel\s+free\s+to\s+reach\s+out\b', 'gi'),
    (r'\blet\s+me\s+know\s+if\s+you\s+need\s+anything\b', 'gi'),
    (r'\bin\s+this\s+article,?\s+we\s+will\s+explore\b', 'gi'),
    (r"\blet'?s\s+dive\s+in!?\b", 'gi'),
]

SYCOPHANTIC = [
    (r"\byou'?re\s+absolutely\s+right\b", 'gi'),
    (r"\bthat'?s\s+a\s+really\s+insightful\b", 'gi'),
    (r"\bthat'?s\s+a\s+great\s+question\b", 'gi'),
    (r'\bexcellent\s+question\b', 'gi'),
]

FILLERS = [
    (r'\bit\s+is\s+important\s+to\s+note\s+that\b', 'gi'),
    (r'\bin\s+terms\s+of\b', 'gi'),
    (r'\bthe\s+reality\s+is\s+that\b', 'gi'),
    (r"\bit'?s\s+important\s+to\s+note\s+that\b", 'gi'),
]

GENERIC_CONCLUSIONS = [
    (r'\bthe\s+future\s+looks\s+bright\b', 'gi'),
    (r'\bonly\s+time\s+will\s+tell\b', 'gi'),
    (r'\bone\s+thing\s+is\s+certain\b', 'gi'),
    (r'\bas\s+we\s+move\s+forward\b', 'gi'),
]

LETS_PATTERNS = [
    (r"\blet'?s\s+explore\b", 'gi'),
    (r"\blet'?s\s+take\s+a\s+look\b", 'gi'),
    (r"\blet'?s\s+break\s+this\s+down\b", 'gi'),
    (r"\blet'?s\s+examine\b", 'gi'),
    (r"\blet'?s\s+(?:consider|discuss|delve|unpack|walk\s+through)\b", 'gi'),
]

REASONING_ARTIFACTS = [
    (r'\blet\s+me\s+think\s+step\s+by\s+step\b', 'gi'),
    (r'\bbreaking\s+this\s+down\b', 'gi'),
    (r'\bto\s+approach\s+this\s+systematically\b', 'gi'),
    (r"\bhere'?s\s+my\s+thought\s+process\b", 'gi'),
    (r"\bfirst,?\s+let'?s\s+consider\b", 'gi'),
    (r'\bworking\s+through\s+this\s+logically\b', 'gi'),
]

SIGNIFICANCE_INFLATION = [
    (r'\bmarking\s+a\s+(?:pivotal|significant|important)\s+moment\b', 'gi'),
    (r'\ba\s+watershed\s+moment\s+for\b', 'gi'),
    (r'\bin\s+the\s+evolution\s+of\b', 'gi'),
    (r'\ba\s+(?:pivotal|defining)\s+moment\s+in\b', 'gi'),
]

VAGUE_ATTRIBUTIONS = [
    (r'\bexperts\s+(?:believe|say|suggest|agree)\b', 'gi'),
    (r'\bstudies\s+(?:show|suggest|indicate)\b', 'gi'),
    (r'\bresearch\s+(?:shows|suggests|indicates)\b', 'gi'),
    (r'\bindustry\s+leaders\s+(?:agree|believe|say)\b', 'gi'),
]

HOLLOW_INTENSIFIERS = [
    (r'\bgenuine(?:ly)?\b', 'gi'),
    (r'\btruly\b', 'gi'),
    (r'\bquite\s+frankly\b', 'gi'),
    (r'\bto\s+be\s+honest\b', 'gi'),
    (r"\blet'?s\s+be\s+clear\b", 'gi'),
]

EMOTIONAL_FLATLINE = [
    (r'\bwhat\s+surprised\s+me\s+most\b', 'gi'),
    (r'\bi\s+was\s+fascinated\s+to\b', 'gi'),
    (r'\bwhat\s+struck\s+me\s+was\b', 'gi'),
    (r'\bi\s+was\s+excited\s+to\s+learn\b', 'gi'),
    (r'\bthe\s+most\s+interesting\s+(?:part|thing|aspect|piece)\b', 'gi'),
    (r'^[ \t]*interesting\s+(?:part|thing|aspect|piece)(?:\s+of\s+(?:the\s+)?\w+)?\s*:', 'gim'),
]

LINGERING_ATTENTION = [
    (r'\b(?:the|that|this)\s+(?:one\s+)?(?:line|quote|bit|part|idea|point|framing|comment|thing)\s+(?:that\s+)?i\s+keep\s+(?:coming\s+back\s+to|thinking\s+about)\b', 'gi'),
    (r"\bi\s+can'?t\s+stop\s+thinking\s+about\b", 'gi'),
    (r'\bstill\s+thinking\s+about\s+(?:this|that)\s+one\b', 'gi'),
    (r'\b(?:been|be)\s+rattling\s+around\s+(?:in\s+)?my\s+(?:head|brain)\b', 'gi'),
    (r"\bi'?ve\s+been\s+chewing\s+on\s+(?:this|that)\b", 'gi'),
]

NOVELTY_INFLATION = [
    (r"\bthe\s+failure\s+mode\s+nobody'?s?\s+naming\b", 'gi'),
    (r'\ba\s+problem\s+nobody\s+talks\s+about\b', 'gi'),
    (r"\bthe\s+insight\s+everyone'?s?\s+missing\b", 'gi'),
    (r'\bwhat\s+nobody\s+tells\s+you\b', 'gi'),
]

CUTOFF_DISCLAIMERS = [
    (r'\bas\s+of\s+my\s+last\s+update\b', 'gi'),
    (r'\bas\s+of\s+my\s+(?:knowledge\s+)?(?:cut-?off|last\s+training)\b', 'gi'),
    (r"\bi\s+don'?t\s+have\s+access\s+to\s+real-?time\s+(?:data|information)\b", 'gi'),
    (r'\bbased\s+on\s+available\s+information\b', 'gi'),
    (r'\bas\s+an?\s+(?:ai|artificial\s+intelligence|large\s+language|ai\s+language)\s+(?:language\s+)?model\b', 'gi'),
    (r"\bi\s+(?:am|'m)\s+an?\s+(?:ai|artificial\s+intelligence|large\s+language)\s+(?:assistant|model)?\b", 'gi'),
    (r'\bi\s+cannot\s+(?:provide|give|offer)\s+(?:legal|medical|financial|professional)\s+advice\b', 'gi'),
    (r'\bmy\s+training\s+data\s+(?:only\s+)?(?:goes\s+up\s+to|extends\s+to|ends\s+(?:in|at))\b', 'gi'),
]

AI_PLACEHOLDERS = [
    (r'\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose|Pick)[^\]\n]{1,80}\]', 'gi'),
    (r'\[(?:Recipient|Sender|Topic|Subject|Salutation|Closing|Position|Department|Project Name|Company Name|Date)(?:\s+[^\]\n]{0,60})?\]', 'gi'),
    (r'\[(?:INSERT|FILL\s+IN|ADD|TODO|TBD|PLACEHOLDER)[^\]\n]{0,80}\]', 'g'),
    (r'\b(?:19|20)\d{2}-XX-XX\b', 'g'),
    (r'\bXX\/XX\/(?:19|20)\d{2}\b', 'g'),
    (r'<!--\s*(?:add|fill\s+in|insert|todo|placeholder)[^>]{0,120}-->', 'gi'),
]

AI_CITATION_MARKUP = [
    (r'\bcite(?:turn|news|search|navigation)\d+(?:search|turn|news|navigation)\d+', 'gi'),
    (r'contentReference\s*\[oaicite:[^\]]+\]\s*\{[^}]*\}', 'gi'),
    (r'\boai_citation\b', 'gi'),
    (r'\[attached_file:\d+\]', 'gi'),
    (r'\bgrok_card\b', 'gi'),
]

AI_UTM_SOURCE = [
    (r'[?&]utm_source=(?:chatgpt|openai|copilot|claude|grok|gemini|perplexity)(?:\.com|\.ai)?\b', 'gi'),
    (r'[?&]referrer=(?:chatgpt|copilot|grok|claude|gemini|perplexity)\.(?:com|ai)\b', 'gi'),
]

TEMPLATE_PHRASES = [
    (r'\ba\s+\w+\s+step\s+(?:towards?|forward\s+for)\b', 'gi'),
    (r"\bwhether\s+you'?re\s+\w+\s+or\s+\w+", 'gi'),
    (r'\bi\s+recently\s+had\s+the\s+pleasure\s+of\b', 'gi'),
]

FALSE_CONCESSION = [
    (r'\bwhile\s+\w+\s+is\s+impressive\b', 'gi'),
    (r'\balthough\s+\w+\s+has\s+made\s+strides\b', 'gi'),
    (r'\bdespite\s+\w+\s+challenges?\b', 'gi'),
]

RHETORICAL_QUESTIONS = [
    (r'\bbut\s+what\s+does\s+this\s+mean\s+for\b', 'gi'),
    (r'\bso\s+why\s+should\s+you\s+care\b', 'gi'),
    (r"\bwhat'?s\s+next\?\s*", 'gi'),
]

HEDGE_STACK = [
    (r'\b(?:could|may|might)\s+(?:(?!not\b|never\b|hardly\b|scarcely\b|barely\b)\w+\s+)?(?:potentially|eventually|ultimately|possibly|conceivably)\b', 'gi'),
    (r'\b(?:potentially|eventually|ultimately)\s+(?:could|may|might)\b', 'gi'),
]

FUTURE_NARRATIVE = [
    (r'\b(?:may|could|will|is\s+(?:poised|set)\s+to)\s+become\s+(?:one\s+of\s+)?(?:the\s+)?(?:most\s+)?\w+\s+(?:narratives?|stories|developments?|trends?|movements?|chapters?|themes?|forces?)\b', 'gi'),
    (r'\bone\s+of\s+the\s+most\s+important\s+(?:narratives?|stories|trends?|themes?)\s+of\s+the\s+(?:next|coming)\s+\w+\b', 'gi'),
]

REAL_ACTUAL_INFLATION = [
    (r'\b(?:real|actual|genuine|true)\s+(?:on-?chain\s+)?(?:tokenomics|economics|utility|adoption|sustainability|impact|revenue|fundamentals|demand|value|innovation|traction)\b', 'gi'),
]

FORMULAIC_OPENERS = [
    (r'\bin\s+the\s+(?:rapidly\s+|ever-?\s*)?(?:evolving|changing|expanding|growing|shifting)\s+(?:world|landscape|realm|space|field|domain|era)\s+of\b', 'gi'),
    (r'\bin\s+(?:an?|the)\s+(?:digital\s+)?age\s+(?:where|of)\b', 'gi'),
    (r'\bas\s+(?:we|the\s+world|society|industries?)\s+(?:continue|move|navigate|enter)\s+(?:to\s+)?(?:evolve|forward|into|through)\b', 'gi'),
    (r'\bhas\s+emerged\s+as\s+(?:a|the|one\s+of)\s+(?:leading|key|major|critical|essential|fundamental|pivotal|prominent|dominant|important)\s+\w+', 'gi'),
    (r'\bhas\s+become\s+increasingly\s+(?:important|critical|popular|relevant|prominent|essential)\b', 'gi'),
]

SPECULATIVE_OPENERS = [
    (r'\b(?:imagine|picture|envision)(?:\s*,[^,\n]{1,30},)?\s+a\s+(?:world|future|reality)\s+(?:where|in\s+which)\b', 'gi'),
]

LAUNCH_INTROS = [
    (r"(?<=^|[.!?]\s|\n)Meet\s+[A-Z][\w'-]{1,29}\s*,\s*(?:your\s+new\s+(?:favorite|go-to)\b|the\s+new\s+(?:home\s+of\b|way\s+to\b|standard\s+(?:in|for)\b|(?:standard|way|home)(?=\s*(?:[.!?,;:\u2013\u2014]|$))))", 'g'),
    (r"(?<=^|[.!?]\s|\n)[Tt]hink\s+[A-Z][\w'-]{1,29}\s+meets\s+[A-Z][\w'-]{1,29}\b", 'g'),
]

CROWD_CONTRAST = [
    (r'\bwhile\s+(?:everyone\s+else|the\s+(?:industry|market|competition)|others)\s+(?:was|were|is|are)\s+still\s+(?:busy\s+)?(?:(?:debat|deliberat|hesitat|theoriz|philosophiz|pontificat|speculat|argu)ing|(?:dither|bicker)ing)\b', 'gi'),
    (r'\bwhile\s+(?:everyone\s+else|the\s+(?:industry|market|competition)|others)\s+(?:was\s+|were\s+)?(?:busy\s+)?(?:writing|wrote)\s+think-?\s?pieces\b', 'gi'),
    (r'\bwhile\s+(?:everyone\s+else|the\s+(?:industry|market|competition)|others)\s+(?:was\s+|were\s+|is\s+|are\s+)?(?:still\s+)?play(?:ed|ing|s)?\s+catch[-\s]?up\b', 'gi'),
]

FAKE_CASUAL_PROPS = [
    (r"\*\s?(?:checks\s+notes|chef['\u2019]s\s+kiss|mic\s+drop|takes\s+a\s+deep\s+breath|sips\s+(?:coffee|tea)|nervous\s+laughter)\s?\*", 'gi'),
    (r'\(\s?(?:yes|no)\s?,\s?(?:really|seriously)\s?\)', 'gi'),
]

PERFORMED_INSIGHT = [
    ('\\bsit(?:s|ting)?\\s+with\\s+(?:that|this)(?=\\s*(?:[.!?,;:)\\u2013\\u2014\\u2019"\']|for\\s+a\\s+(?:moment|minute|second|beat)\\b|$))(?:\\s+for\\s+a\\s+(?:moment|minute|second|beat))?', 'gi'),
    (r'\bsit(?:s|ting)?\s+with\s+(?:the|your)\s+(?:discomfort|tension|uncertainty|ambiguity|grief|unease)\b', 'gi'),
    (r"\b(?:that|this|it|which)(?:['\u2019]s|\s+(?:is|was))\s+not\s+nothing\b", 'gi'),
    (r'\byou\s+already\s+know\s+the\s+answer\b', 'gi'),
    (r"\b(?:do\s+not|don['\u2019]t)\s+(?:have\s+to\s+)?take\s+my\s+word\s+for\s+it\b", 'gi'),
    (r'(?<=^|[.!?]\s|\n)Turns\s+out\b', 'g'),
    (r"(?:['\u2019]s|\b(?:is|was|are|were))\s+the\s+(?:whole|entire)\s+(?:point|game|ballgame|trick|pitch|idea|play|business\s+model|value\s+proposition)\b", 'gi'),
    (r"\b(?:that|this)(?:['\u2019]s|\s+(?:is|was))\s+the\s+part\s+(?:that|I|you|we|nobody|no\s+one|most\s+people)\b", 'gi'),
    (r"\bthe\s+only\s+[\w'\u2019-]+\s+that\s+(?:matters|counts)\b", 'gi'),
    (r'\bis\s+dead\s*[.;,:\u2013\u2014]\s*long\s+live\b', 'gi'),
    (r"\b(?:that|this)(?:['\u2019]s|\s+(?:is|was))\s+why\s+[^.!?\n]{0,60}\s+mattered\b", 'gi'),
]

STAGED_DISCOVERY = [
    (r'\b(?:turned|turns|turning)\s+out\s+to\s+be\s+the\s+(?:least|most)\s+(?:interesting|important|surprising|revealing|valuable|useful)\s+(?:part|thing|piece|bit)\b', 'gi'),
    (r'\bthe\s+real\s+story\s+(?:here\s+)?(?:is|was)\b(?=\s+(?:the|that|how|why|what)\b)', 'gi'),
]

NEGATION_CHAIN = [
    (r"(?<=^|[.!?]\s|\n|[:\u2013\u2014]\s)No\s+(?!matter\b|one\b|doubt\b|longer\b|way\b|less\b|more\b|such\b|other\b|means\b)[a-z'’-]+(?:\s+(?!(?:in|on|at|of|to|for|with|from|by|is|are|was|were|be|been|being|will|would|can|could|should|shall|may|might|must|have|has|had|do|does|did)\b)[a-z'’-]+)?(?:\s*,\s*(?:and\s+|or\s+|just\s+)?no\s+(?!matter\b|one\b|doubt\b|longer\b|way\b|less\b|more\b|such\b|other\b|means\b)[a-z'’-]+(?:\s+(?!(?:in|on|at|of|to|for|with|from|by|is|are|was|were|be|been|being|will|would|can|could|should|shall|may|might|must|have|has|had|do|does|did)\b)[a-z'’-]+)?){2,}", 'gm'),
    (r"\b(?:did\s+not|didn['\u2019]t)\s+[a-z]+[^,.;!?\n]{0,20},\s*(?:did\s+not|didn['\u2019]t)\s+[a-z]+", 'gi'),
    ('\\b(?:do\\s+not|don[\'\\u2019]t)\\s+(?:just\\s+)?(\\w+)\\s+it\\b[^.!?\\n]{0,60}[.!?;:,][\\s\'"\\u201d\\u2019]*(?:just\\s+)?\\1\\s+it\\b', 'gi'),
]

DEV_BLOG_BOILERPLATE = [
    (r'\bit\s+just\s+works\b(?!\s+out\b(?![-\s]+of[-\s]+the[-\s]+box\b))', 'gi'),
    (r'\bzero[-\s]config(?:uration)?\b', 'gi'),
    (r'\bsane\s+defaults\b', 'gi'),
    (r'\b(?:hold|fit|fits|holds)\s+in\s+your\s+head\b', 'gi'),
]

PARENTHETICAL_HEDGE = [
    (r'\(\s*(?:and\s+)?(?:increasingly|notably|importantly|crucially|interestingly|perhaps)[,]?\s+[^)]{3,60}\)', 'gi'),
    (r'\(\s*or\s+more\s+(?:precisely|accurately|specifically)[,]?\s+[^)]{3,60}\)', 'gi'),
    (r'\(\s*though\s+to\s+be\s+fair[,]?\s+[^)]{3,60}\)', 'gi'),
    (r'\(\s*at\s+least\s+(?:in\s+)?(?:theory|principle|part)[,]?\s+[^)]{0,60}\)', 'gi'),
]

CONFIDENCE_CALIBRATION = [
    (r'\binterestingly\b', 'gi'),
    (r'\bsurprisingly\b', 'gi'),
    (r'\bimportantly\b', 'gi'),
    (r'\bsignificantly\b', 'gi'),
    (r'\bcertainly\b', 'gi'),
    (r'\bundoubtedly\b', 'gi'),
    (r'\bwithout\s+a\s+doubt\b', 'gi'),
]

SOCIAL_CTA_CLOSER = [
    (r"\bthis\s+one['’]?s?\s+(?:is\s+)?(?:well\s+|totally\s+|absolutely\s+|definitely\s+|really\s+|truly\s+|easily\s+|more\s+than\s+)?worth\s+(?:your\s+time|the\s+read|a\s+read|every\s+(?:minute|second)|reading|watching|a\s+listen|a\s+watch|a\s+look|it)\b", 'gi'),
    (r"\bthis\s+one['’]?s?\s+(?:is\s+)?a\s+must[-\s]?(?:read|watch|listen|see)\b", 'gi'),
    (r"\b(?:highly|strongly|can['’]?t|cannot)\s+recommend\w*\s+(?:giving\s+)?(?:this|it)\s+(?:one\s+)?a\s+(?:read|listen|watch|look|go)\b", 'gi'),
    (r'\bdo\s+yourself\s+a\s+favou?r\s+and\s+(?:read|watch|check\s+out)\s+(?:this|it)\b', 'gi'),
    (r"\byou\s+(?:really\s+)?(?:won['’]?t|do\s*n['’]?t|will\s+not|do\s+not)\s+want\s+to\s+miss\s+this(?:\s+one)?(?=\s*(?:[:.!\n]|$))", 'gi'),
    (r'(?<=^|[,.!?:\n]\s{0,4})(?:you\s+can\s+)?thank\s+me\s+later\b', 'gim'),
    (r'(?<=^|[.!?:\n]\s{0,4})save\s+this\s+(?:one\s+)?for\s+later\b', 'gim'),
    (r'\bbookmark\s+this(?:\s+(?:one|post|thread))?(?=\s*(?:[:.!\n]|$))', 'gi'),
    (r"\bdo\s*n['’]?t\s+sleep\s+on\s+this\b", 'gi'),
    (r"\btrust\s+me,?\s+(?:on\s+this|you['’]?ll)\b", 'gi'),
]

TIER3_PHRASES = [
    (r'\bemerging\s+(?:sector|space|category|industry)\b', 'gi'),
    (r'\bthe\s+integration\s+of\b', 'gi'),
    (r'\bthe\s+intersection\s+of\b', 'gi'),
    (r'\bcommunity-?driven\b', 'gi'),
    (r'\blong-?term\s+sustainability\b', 'gi'),
    (r'\buser\s+engagement\b', 'gi'),
    (r'\bdecentralized\s+compute\b', 'gi'),
    (r'\b(?:sustainable\s+)?reward\s+emissions?\b', 'gi'),
    (r'\btokenized\s+incentive\s+structures?\b', 'gi'),
    (r'\bdesigned\s+for\s+long-?term\b', 'gi'),
]

TITLE_CASE_HEADER = (r'^(?:#{1,6}[ \t]+)?([A-Z][a-z]+(?:[ \t]+(?:[A-Z][a-z]+|A|I|[A-Z]{2,}|and|or|of|the|in|for|to|a|an))+[ \t]+[A-Z][a-z]+)[ \t]*$', 'gm')

FUNCTION_WORD = (r'\b(?:And|Or|Of|The|In|For|To|A|An)\b', '')

MD_HEADING_PREFIX = (r'^#{1,6}[ \t]+', '')

HEX_COLOUR = (r'^(?=[0-9a-f]*\d)(?:[0-9a-f]{6}|[0-9a-f]{8})$', 'i')

CPP_DIRECTIVE = (r'^(?:include|define|undef|if|ifdef|ifndef|elif|else|endif|pragma|error|warning|line)$', '')


UNNECESSARY_HYPHENATION = [
    ((r'\bresearch-impact\s+aggregat(?:or|ion)s?\b', 'g'), lambda m: m.replace('research-impact', 'research impact', 1)),
    ((r'\bdata-source\s+strateg(?:y|ies)\b', 'g'), lambda m: m.replace('data-source', 'data source', 1)),
    ((r'\bPython-package\s+usage\b', 'g'), lambda m: m.replace('Python-package', 'Python package', 1)),
    ((r'\bRust-crate\s+usage\b', 'g'), lambda m: m.replace('Rust-crate', 'Rust crate', 1)),
    ((r'\bsingle-Project\s+Manifest\b', 'g'), lambda m: m.replace('single-Project', 'single Project', 1)),
    ((r'\btotal-downloads\s+figures?\b', 'g'), lambda m: m.replace('total-downloads', 'total downloads', 1)),
    ((r'\blife-sciences-native\s+citation\s+count\b', 'g'), 'citation count from a life sciences source'),
    ((r'\bcode-base\b', 'g'), lambda m: m.replace('-', '', 1)),
    ((r'\bdata-set\b', 'g'), lambda m: m.replace('-', '', 1)),
    ((r'\btime-frame\b', 'g'), lambda m: m.replace('-', '', 1)),
    ((r'\broad-map\b', 'g'), lambda m: m.replace('-', '', 1)),
    ((r'\bin\s+real-time(?=\s*(?:[,.!?;:]|$)|\s+(?:(?:across|as|automatically|because|but|continuously|during|dynamically|every|for|from|immediately|instantly|on|simultaneously|through|throughout|until|via|when|while|with|without)\b))', 'gi'), 'in real time'),
    ((r'\b(?:for|over)\s+the\s+long-term(?=\s*(?:[,.!?;:]|$)|\s+(?:across|because|but|by|during|for|from|on|through|throughout|until|via|when|while|with|without)\b)', 'gi'),
     lambda m: re.sub('long-term', 'long term', m, count=1, flags=re.I | re.A)),
    ((r'\b(?:functions?|functioned|functioning|operates?|operated|operating|runs?|ran|running|works?|worked|working)\s+out-of-the-box\b', 'gi'),
     lambda m: re.sub('out-of-the-box', 'out of the box', m, count=1, flags=re.I | re.A)),
]

# Script_Extensions=Han|Hiragana|Katakana as Node 24 (Unicode 17.0) defines
# them; Python re has no \p{...}.
CJK_RANGES = [
    (0x00b7, 0x00b7), (0x0305, 0x0305), (0x0323, 0x0323), (0x2e80, 0x2e99),
    (0x2e9b, 0x2ef3), (0x2f00, 0x2fd5), (0x2ff0, 0x2fff), (0x3001, 0x3003),
    (0x3005, 0x3011), (0x3013, 0x301f), (0x3021, 0x302d), (0x3030, 0x3035),
    (0x3037, 0x303f), (0x3041, 0x3096), (0x3099, 0x30ff), (0x3190, 0x319f),
    (0x31c0, 0x31e5), (0x31ef, 0x31ff), (0x3220, 0x3247), (0x3280, 0x32b0),
    (0x32c0, 0x32cb), (0x32d0, 0x3370), (0x337b, 0x337f), (0x33e0, 0x33fe),
    (0x3400, 0x4dbf), (0x4e00, 0x9fff), (0xa700, 0xa707), (0xf900, 0xfa6d),
    (0xfa70, 0xfad9), (0xfe45, 0xfe46), (0xff61, 0xff9f), (0x16fe2, 0x16fe3),
    (0x16ff0, 0x16ff6), (0x1aff0, 0x1aff3), (0x1aff5, 0x1affb),
    (0x1affd, 0x1affe), (0x1b000, 0x1b122), (0x1b132, 0x1b132),
    (0x1b150, 0x1b152), (0x1b155, 0x1b155), (0x1b164, 0x1b167),
    (0x1d360, 0x1d371), (0x1f200, 0x1f200), (0x1f250, 0x1f251),
    (0x20000, 0x2a6df), (0x2a700, 0x2b81d), (0x2b820, 0x2cead),
    (0x2ceb0, 0x2ebe0), (0x2ebf0, 0x2ee5d), (0x2f800, 0x2fa1d),
    (0x30000, 0x3134a), (0x31350, 0x33479),
]
CJK_RE = re.compile('[' + ''.join(
    '\\U%08x' % a if a == b else '\\U%08x-\\U%08x' % (a, b) for a, b in CJK_RANGES) + ']')

# Python re rejects JavaScript's variable-width lookbehinds. Each one is
# rewritten as an alternation of fixed-width lookbehinds with the same
# meaning (JS ^ is \A without /m, any line start with /m).
_LB_SENTENCE = '(?:\\A|(?<=[.!?]' + WS + ')|(?<=\\n))'
_LB_CTA_COMMA = '(?:\\A|(?<=' + LT + ')' + ''.join(
    '|(?<=[,.!?:\\n]' + WS * k + ')' for k in range(5)) + ')'
_LB_CTA = '(?:\\A|(?<=' + LT + ')' + ''.join(
    '|(?<=[.!?:\\n]' + WS * k + ')' for k in range(5)) + ')'
LOOKBEHIND_REWRITES = {
    ('(?<=^|[.!?]\\s|\\n)', 'g'): _LB_SENTENCE,
    ('(?<=^|[.!?]\\s|\\n|[:\\u2013\\u2014]\\s)', 'gm'):
        '(?:\\A|(?<=' + LT + ')|(?<=[.!?]' + WS + ')|(?<=[:\\u2013\\u2014]' + WS + '))',
    ('(?<=^|[,.!?:\\n]\\s{0,4})', 'gim'): _LB_CTA_COMMA,
    ('(?<=^|[.!?:\\n]\\s{0,4})', 'gim'): _LB_CTA,
}
# /—|(?<=\s)--(?=\s|$)|(?<=^|\s)--(?=\s)/gm
EM_DASH_RE = py_re('—|(?<=' + WS + ')--(?=' + WS + '|\\Z)|(?:\\A|(?<=' + WS + '))--(?=' + WS + ')')


def compile_js(pattern):
    source, flags = pattern
    for (prefix, pflags), replacement in LOOKBEHIND_REWRITES.items():
        if flags == pflags and source.startswith(prefix):
            from aiw_jscompat import translate
            body = replacement + translate(source[len(prefix):], flags)
            return py_re(body, re.IGNORECASE if 'i' in flags else 0)
    return js_re(source, flags)


TIER3_LOOKUP = {}
for _word in TIER3:
    TIER3_LOOKUP[_word] = _word
    if '-' in _word:
        TIER3_LOOKUP[_word.replace('-', '')] = _word

FUNC_WORDS = frozenset([
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at', 'by', 'for', 'with',
    'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can',
    'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'there', 'here',
    'we', 'our', 'us', 'i', 'you', 'your', 'he', 'she', 'his', 'her', 'him', 'not', 'no', 'so',
    'if', 'then', 'than', 'when', 'where', 'which', 'who', 'what', 'how', 'why', 'because',
])

NON_HIGHLIGHT_TYPES = frozenset([
    'punct-distribution', 'cross-para-burstiness', 'fnword-trigram-entropy',
    'smart-punct-signature', 'normalization-flag', 'uniformity', 'em-dash',
    'formatting', 'tier3', 'tier3-phrase', 'tier3-phrase-cluster',
    'hashtag-stuff', 'bullet-np-list', 'unnecessary-hyphenation',
])

VALID_CONTEXT_MODES = ('general', 'technical', 'marketing', 'personal')
VALID_SOURCE_MODES = ('plain', 'rendered-markdown')
MAX_WORDS = 10000

SEVERITY_LABELS = {'critical': 'P0', 'high': 'P1', 'medium': 'P2', 'low': 'P3'}

# Frequently used regexes.
RE_WORD_RUN = js_re(r'\S+', 'g')
RE_TOKEN = js_re(r"[\w'-]+", 'g')
RE_PARA_SPLIT = js_re(r'\n\s*\n', '')
RE_SENT_SPLIT = js_re(r'[.!?]+', '')
RE_CRLF_SPLIT = js_re(r'\r?\n', '')
RE_ANY_EOL_SPLIT = js_re(r'\r\n|\n|\r', '')
RE_LINE = js_re(r'[^\r\n]*(?:\r\n|\n|\r|$)', 'g')
RE_LINE_TERMINATOR_END = js_re(r'(?:\r\n|\n|\r)$', '')
RE_FENCE_LINE_G = js_re(r'^[ \t]{0,3}(`{3,}|~{3,})([^\n]*)$', 'gm')
RE_FENCE_LINE = js_re(r'^[ \t]{0,3}(`{3,}|~{3,})([^\n]*)$', '')
RE_FENCE_CLOSE_TAIL = js_re(r'^[ \t]*\r?$', '')
RE_QUOTE_LINE = js_re(r'^\s*>\s', '')
RE_INDENTED = js_re(r'^(?: {4}|\t)\S', '')
RE_INLINE_SPAN = js_re(r'(`+)(?:(?!\1)[^\n])+\1', 'g')
RE_LIST_MARKER = js_re(r'^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:\s|$)', '')
RE_NON_SPACE_START = js_re(r'^\S', '')
RE_FM_DELIM = js_re(r'^---[ \t]*$', '')
RE_FM_COMMENT = js_re(r'^[ \t]*#', '')
RE_FM_YAML_KEY = js_re(r'''^[ \t]*(?:[A-Za-z0-9_.-]+|"[^"\r\n]+"|'[^'\r\n]+')[ \t]*:''', '')
RE_BLANK_LINE = js_re(r'^\s*$', '')
RE_YAML_KEY = js_re(r'^([ \t]*)(?:-[ \t]+)?[a-z_][a-z0-9_.-]*[ \t]*:(.*)$', '')
RE_LEADING_INDENT = js_re(r'^[ \t]*', '')
RE_TABLE_DELIM = js_re(r'^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$', '')
RE_ALNUM = js_re(r'[a-z0-9]', 'i')
RE_TRAILING_CR = js_re(r'\r$', '')
RE_HASHTAG = js_re(r'(?:^|\W)#(\w[\w-]*)', 'g')
RE_DIGITS = js_re(r'^\d+$', '')
RE_VERB = js_re(r'\b(?:is|are|was|were|has|have|had|will|would|should|must|do|does|did|can|could|may|might|am|been|being)\b', 'i')
RE_BULLET_FENCE = js_re(r'^\s*(?:```|~~~)', '')
# SEPARATOR_DASH_RE is /^\s*<rest>/gm. Its leading \s* is run by hand in
# count_separator_dashes(): Python's backtracking made the plain regex
# quadratic on long blank (masked) regions.
RE_SEPARATOR_DASH_REST = js_re(r'(?:[-*+]|\d+[.)])\s+(?:\*\*[^*\n]+\*\*|\[[^\]\n]+\]\([^)\n]*\))(?:[ \t]*(?:\([^)\n]*\)|`[^`\n]+`))?[ \t]*—', 'gm')
RE_LT = py_re(LT)
RE_NOT_WS = py_re(NOT_WS)
RE_ISO_DATE = js_re(r'^\d{4}-\d{2}-\d{2}$', '')
RE_SEMVER = js_re(r'^v?\d+\.\d+\.\d+', '')
RE_CURLY = js_re('[“”‘’]', '')
RE_OXFORD = js_re(r'\b\w+,\s+\w+,\s+and\s+\w+', 'g')
RE_DOUBLE_SPACE = js_re(r'[^.!?]  +', 'g')
RE_MISSING_APOS = js_re(r'\b(?:dont|wont|cant|isnt|wasnt|shouldnt|wouldnt|couldnt|youre|theyre|its\s+a\s+\w+ing)\b', 'i')
RE_PUNCT = js_re('[,;:—()]', 'g')
RE_BOLD = js_re(r'\*\*[^*]+\*\*', 'g')
RE_TERMINATOR_RUN = js_re(r'[.!?]+', 'g')
RE_FIRST_NON_SPACE = js_re(r'\S', 'g')
RE_ROLEPLAY_MARKER = re.compile(r'(?<!\*)\*([^*\n]{1,80}?)\*(?!\*)')
RE_ROLEPLAY_VERBS = js_re(r'^(?:nods|sighs|laughs|smiles|frowns|shrugs|grins|winks|chuckles|gasps|pauses|thinks|wonders|whispers|shouts|gestures|raises|leans|turns|looks|glances|smirks|blinks|nodding|sighing|laughing|smiling|thinking|gesturing)\b', 'i')

HYPHENATION_MASKS = [
    (r'^[ \t]*>[^\n]*$', 'gm'),
    (r'\b(?:https?:\/\/|www\.)[^\s<>]+', 'gi'),
    (r'<[!?/]?[a-z][^<>\n]*>', 'gi'),
    (r'(?<![a-z0-9_-])--?[a-z0-9][a-z0-9-]{0,127}', 'gi'),
    (r'(?:[a-z]:[\\/]|\.{1,2}[\\/]|~[\\/]|[\\/])[a-z0-9_.-]{1,255}', 'gi'),
    (r'(?:[a-z]:[\\/]|(?:\.\.?[\\/])?)(?:[a-z0-9_.-]{1,64}[\\/]){1,128}[a-z0-9_.-]{1,64}', 'gi'),
    (r'\b[a-z0-9_.]{0,63}-[a-z0-9_.-]{1,64}[\\/]', 'gi'),
    (r'\b[a-z0-9_.-]{1,64}-[a-z0-9_.-]{1,64}\.[a-z0-9]{1,16}\b', 'gi'),
    (r'[.#][a-z_][a-z0-9_.-]{0,63}-[a-z0-9_.-]{1,64}\b', 'gi'),
    (r'@[a-z0-9_.-]{1,64}\/[a-z0-9_.-]{1,64}-[a-z0-9_.-]{1,64}(?:@[^\s,;)\]}]{1,32})?', 'gi'),
    (r'\b[a-z0-9_.-]{1,64}-[a-z0-9_.-]{1,64}@[~^]?v?\d[a-z0-9*_.+-]{0,31}\b', 'gi'),
    (r'\b(?:[a-z0-9_.-]{0,64}\d[a-z0-9_.-]{0,64}-[a-z0-9_.-]{1,64}|[a-z0-9_.-]{1,64}-[a-z0-9_.-]{0,64}\d[a-z0-9_.-]{0,64})\b', 'gi'),
    (r'\b[a-z_][a-z0-9_.]{0,63}(?:-[a-z0-9_.]{1,64}){1,8}(?=[ \t]*[=:])', 'gi'),
    (r'\b[a-z_][a-z0-9_.]{0,63}(?:-[a-z0-9_.]{1,64}){1,8}(?=[ \t]+(?:npm[ \t]+)?(?:package|module|class|selector|config(?:uration)?[ \t]+key|key|identifier|property|setting|token|slug|command|option)\b)', 'gi'),
    (r'\b(?:(?:file(?:name)?|directory|folder|package|module|class|selector|config(?:uration)?[ \t]+key|identifier|property|setting|token|slug|command|option)(?:[ \t]+(?:named|called|is|was))?|key[ \t]+(?:named|called|is|was))[ \t]+(?:@[a-z0-9_.-]{1,64}\/)?[a-z_][a-z0-9_.]{0,63}(?:-[a-z0-9_.]{1,64}){1,8}\b', 'gi'),
    (r'\b(?:npm|pnpm|yarn)[ \t]+(?:add|install)[ \t]+(?:@[a-z0-9_.-]{1,64}\/)?[a-z0-9_.]{1,64}(?:-[a-z0-9_.]{1,64}){1,8}', 'gi'),
]


# ═══ Helpers ═══════════════════════════════════════════════════════════════

def _fsum(values):
    # Array.reduce((a, b) => a + b, 0): plain left-to-right float addition.
    total = 0
    for v in values:
        total += v
    return total


def count_words(text):
    return len(exec_all(RE_WORD_RUN, text))


def tokenize(text):
    return [m.group(0) for m in exec_all(RE_TOKEN, js_lower(text))]


def get_paragraphs(text):
    return [p for p in RE_PARA_SPLIT.split(text) if len(js_trim(p)) > 0]


def get_sentences(text):
    return [s for s in RE_SENT_SPLIT.split(text) if len(js_trim(s)) > 5]


def match_patterns(text, patterns, category, severity):
    issues = []
    for pattern in patterns:
        for m in exec_all(compile_js(pattern), text):
            issues.append({
                'type': category,
                'text': m.group(0),
                'index': m.start(),
                'severity': severity,
                'suggestion': None,
            })
    return issues


def blank_range(chars, start, end):
    for i in range(start, min(end, len(chars))):
        if chars[i] != '\n':
            chars[i] = ' '


def split_terminated_lines(text):
    """Lines from /[^\\r\\n]*(?:\\r\\n|\\n|\\r|$)/g, stopping at the first empty match."""
    lines = []
    pos = 0
    while True:
        m = RE_LINE.search(text, pos)
        if m is None or m.group(0) == '':
            break
        body = RE_LINE_TERMINATOR_END.sub('', m.group(0), count=1)
        lines.append((body, m.start(), m.start() + len(body)))
        pos = m.end()
    return lines


# ═══ Normalization ═════════════════════════════════════════════════════════

def normalize_text(text, source_map):
    flags = {'zeroWidth': 0, 'homoglyph': 0, 'roleplay': 0}

    # 1. Strip zero-width characters.
    chars = []
    next_map = []
    for i, ch in enumerate(text):
        if ch in ZERO_WIDTH:
            flags['zeroWidth'] += 1
            continue
        chars.append(ch)
        next_map.append(source_map[i])
    out = ''.join(chars)
    smap = next_map

    # 2. Swap Cyrillic / Greek lookalikes back to Latin.
    swapped = []
    for ch in out:
        if 'Ͱ' <= ch <= 'ӿ':
            swap = CYRILLIC_LOOKALIKES.get(ch) or GREEK_LOOKALIKES.get(ch)
            if swap:
                flags['homoglyph'] += 1
                swapped.append(swap)
                continue
        swapped.append(ch)
    out = ''.join(swapped)

    # 3. Strip *roleplay-action* markers. The JS regex carries /u, so {1,80}
    # counts code points: run it on the joined string and map back to units.
    real = from_u16(out)
    if len(real) != len(out):
        unit_at = []
        u = 0
        for ch in real:
            unit_at.append(u)
            u += 2 if ord(ch) > 0xFFFF else 1
        unit_at.append(u)
    else:
        unit_at = None
    pieces = []
    new_map = []
    cursor = 0
    for m in RE_ROLEPLAY_MARKER.finditer(real):
        if not RE_ROLEPLAY_VERBS.search(to_u16(m.group(1))):
            continue
        start = unit_at[m.start()] if unit_at else m.start()
        end = unit_at[m.end()] if unit_at else m.end()
        pieces.append(out[cursor:start])
        new_map.extend(smap[cursor:start])
        flags['roleplay'] += 1
        cursor = end
    pieces.append(out[cursor:])
    new_map.extend(smap[cursor:])
    return ''.join(pieces), flags, new_map


# ═══ Markdown masking helpers ══════════════════════════════════════════════

def fence_ranges(text):
    ranges = []
    open_fence = None
    for m in exec_all(RE_FENCE_LINE_G, text):
        marker = m.group(1)
        if open_fence is None:
            open_fence = (marker[0], len(marker), m.start())
        elif (marker[0] == open_fence[0] and len(marker) >= open_fence[1]
              and RE_FENCE_CLOSE_TAIL.search(m.group(2))):
            ranges.append((open_fence[2], m.end()))
            open_fence = None
    if open_fence is not None:
        ranges.append((open_fence[2], len(text)))
    return ranges


def in_fence_range(ranges, index):
    return any(a <= index < b for a, b in ranges)


def inline_code_ranges(text):
    runs = []
    i, n = 0, len(text)
    while i < n:
        if text[i] == '\n':
            runs.append(None)
            i += 1
            continue
        if text[i] != '`':
            i += 1
            continue
        start = i
        while i < n and text[i] == '`':
            i += 1
        runs.append((start, i, i - start))

    ranges = []
    line_start = 0
    while line_start < len(runs):
        try:
            line_end = runs.index(None, line_start)
        except ValueError:
            line_end = len(runs)
        next_by_length = {}
        next_same = [None] * (line_end - line_start)
        for j in range(line_end - 1, line_start - 1, -1):
            next_same[j - line_start] = next_by_length.get(runs[j][2])
            next_by_length[runs[j][2]] = j
        j = line_start
        while j < line_end:
            close = next_same[j - line_start]
            if close is None:
                j += 1
                continue
            ranges.append((runs[j][0], runs[close][1]))
            j = close + 1
        line_start = line_end + 1
    return ranges


def mask_code(text):
    chars = list(text)
    for a, b in fence_ranges(text):
        blank_range(chars, a, b)
    without_fences = ''.join(chars)
    for a, b in inline_code_ranges(without_fences):
        blank_range(chars, a, b)
    return ''.join(chars)


def initial_frontmatter_range(text):
    lines = split_terminated_lines(text)
    first = lines[0][0] if lines else ''
    if first.startswith('﻿'):
        first = first[1:]
    if len(lines) < 3 or not RE_FM_DELIM.search(first):
        return None
    closing = -1
    for i in range(1, len(lines)):
        if RE_FM_DELIM.search(lines[i][0]):
            closing = i
            break
    if closing == -1:
        return None
    first_content = None
    for body, _, _ in lines[1:closing]:
        if js_trim(body) and not RE_FM_COMMENT.search(body):
            first_content = body
            break
    if first_content is None or not RE_FM_YAML_KEY.search(first_content):
        return None
    return 0, lines[closing][2]


def _backtick_runs(line):
    runs = []
    i, n = 0, len(line)
    while i < n:
        if line[i] != '`':
            i += 1
            continue
        start = i
        while i < n and line[i] == '`':
            i += 1
        runs.append([start, i, i - start, -1])
    next_by_length = {}
    for j in range(len(runs) - 1, -1, -1):
        runs[j][3] = next_by_length.get(runs[j][2], -1)
        next_by_length[runs[j][2]] = j
    return runs


def mask_html_comments_outside_code(chars):
    source = ''.join(chars)
    lines = source.split('\n')
    offset = 0
    open_fence = None
    in_indented_block = False
    previous_blank = True
    list_context = False
    masked = 0
    closings = []
    k = source.find('-->')
    while k != -1:
        closings.append(k)
        k = source.find('-->', k + 1)
    closing_cursor = 0

    for original_line in lines:
        line_end = offset + len(original_line)
        visible = ''.join(chars[offset:line_end])
        fence_match = RE_FENCE_LINE.search(visible)
        fenced_line = False
        if open_fence is not None:
            fenced_line = True
            if (fence_match and fence_match.group(1)[0] == open_fence[0]
                    and len(fence_match.group(1)) >= open_fence[1]
                    and RE_FENCE_CLOSE_TAIL.search(fence_match.group(2))):
                open_fence = None
        elif fence_match:
            fenced_line = True
            open_fence = (fence_match.group(1)[0], len(fence_match.group(1)))

        indented = bool(RE_INDENTED.search(visible))
        indented_code = (not fenced_line and indented
                         and (in_indented_block or (previous_blank and not list_context)))

        if not fenced_line and not indented_code:
            runs = _backtick_runs(visible)
            run_index = 0
            cursor = 0
            while cursor < len(visible):
                while run_index < len(runs) and runs[run_index][0] < cursor:
                    run_index += 1
                comment_index = visible.find('<!--', cursor)
                run = runs[run_index] if run_index < len(runs) else None
                if run is not None and (comment_index == -1 or run[0] < comment_index):
                    if run[3] != -1:
                        cursor = runs[run[3]][1]
                        run_index = run[3] + 1
                    else:
                        cursor = run[1]
                        run_index += 1
                    continue
                if comment_index == -1:
                    break
                opening = offset + comment_index
                while closing_cursor < len(closings) and closings[closing_cursor] < opening + 2:
                    closing_cursor += 1
                closing = closings[closing_cursor] if closing_cursor < len(closings) else -1
                end = len(source) if closing == -1 else closing + 3
                if closing != -1:
                    closing_cursor += 1
                blank_range(chars, opening, end)
                masked += 1
                cursor = min(len(visible), end - offset)

        visible = ''.join(chars[offset:line_end])
        layout = list(visible)
        if fenced_line:
            blank_range(layout, 0, len(layout))
        else:
            for m in exec_all(RE_INLINE_SPAN, visible):
                blank_range(layout, m.start(), m.end())
        layout_line = ''.join(layout)
        blank = js_trim(layout_line) == ''

        if indented_code:
            in_indented_block = True
        elif not blank:
            in_indented_block = False

        if not blank and not indented_code and not fenced_line:
            if RE_LIST_MARKER.search(layout_line):
                list_context = True
            elif RE_NON_SPACE_START.search(layout_line):
                list_context = False
        previous_blank = blank
        offset = line_end + 1

    return masked


def mask_rendered_markdown(text):
    chars = list(text)
    masked_frontmatter = 0
    fm = initial_frontmatter_range(text)
    if fm:
        blank_range(chars, fm[0], fm[1])
        masked_frontmatter = 1
    masked_comments = mask_html_comments_outside_code(chars)
    return ''.join(chars), masked_frontmatter, masked_comments


def _quote_flags(bodies):
    is_quote = [bool(RE_QUOTE_LINE.search(b)) for b in bodies]
    n = len(is_quote)
    out = []
    for i in range(n):
        prev_q = i > 0 and is_quote[i - 1]
        next_q = i + 1 < n and is_quote[i + 1]
        out.append(is_quote[i] and (prev_q or next_q))
    return out


def mask_multiline_blockquotes(text):
    chars = list(text)
    lines = split_terminated_lines(text)
    quoted = 0
    for (body, start, end), strip in zip(lines, _quote_flags([l[0] for l in lines])):
        if strip:
            blank_range(chars, start, end)
            quoted += 1
    return ''.join(chars), quoted


def strip_multiline_blockquotes(text, source_map):
    raw_lines = RE_CRLF_SPLIT.split(text)
    strip = _quote_flags(raw_lines)
    kept = [i for i in range(len(raw_lines)) if not strip[i]]
    result_text = '\n'.join(raw_lines[i] for i in kept)
    quoted = sum(1 for s in strip if s)

    line_starts = []
    offset = 0
    for i, line in enumerate(raw_lines):
        line_starts.append(offset)
        offset += len(line)
        if i < len(raw_lines) - 1:
            if offset < len(text) and text[offset] == '\r':
                offset += 1
            if offset < len(text) and text[offset] == '\n':
                offset += 1

    mapped = []
    for i, line_index in enumerate(kept):
        start = line_starts[line_index]
        mapped.extend(source_map[start:start + len(raw_lines[line_index])])
        if i < len(kept) - 1:
            sep = start + len(raw_lines[line_index])
            newline_index = sep + 1 if sep < len(text) and text[sep] == '\r' else sep
            mapped.append(source_map[newline_index])
    return result_text, quoted, mapped


def mask_top_level_indented_code(chars):
    lines = ''.join(chars).split('\n')
    offset = 0
    in_block = False
    previous_blank = True
    for line in lines:
        indented = bool(RE_INDENTED.search(line))
        blank = js_trim(line) == ''
        if indented and (in_block or previous_blank):
            blank_range(chars, offset, offset + len(line))
            in_block = True
        elif not blank:
            in_block = False
        previous_blank = blank
        offset += len(line) + 1


def _bare(line):
    return line[:-1] if line.endswith('\r') else line


def mask_yaml_frontmatter(chars):
    lines = ''.join(chars).split('\n')
    first = _bare(lines[0])
    if first.startswith('﻿'):
        first = first[1:]
    if first != '---' or len(lines) < 2 or RE_BLANK_LINE.search(_bare(lines[1])):
        return
    closing = -1
    for i in range(1, len(lines)):
        if _bare(lines[i]) == '---':
            closing = i
            break
    if closing == -1:
        return
    end = 0
    for i in range(closing + 1):
        end += len(lines[i])
        if i < len(lines) - 1:
            end += 1
    blank_range(chars, 0, end)


def mask_yaml_metadata(chars):
    lines = ''.join(chars).split('\n')
    offset = 0
    nested_after_indent = None
    for line in lines:
        bare = _bare(line)
        key = RE_YAML_KEY.search(bare)
        indentation = len(RE_LEADING_INDENT.search(bare).group(0))
        should_mask = False
        if key:
            should_mask = True
            nested_after_indent = len(key.group(1)) if js_trim(key.group(2)) == '' else None
        elif nested_after_indent is not None and js_trim(bare) != '' and indentation > nested_after_indent:
            should_mask = True
        else:
            nested_after_indent = None
        if should_mask:
            blank_range(chars, offset, offset + len(line))
        offset += len(line) + 1


def mask_markdown_tables(chars):
    lines = ''.join(chars).split('\n')
    rows = set()
    for i, line in enumerate(lines):
        candidate = js_trim(line)
        if '---' not in candidate or not RE_TABLE_DELIM.search(candidate):
            continue
        if i > 0 and '|' in lines[i - 1]:
            rows.add(i - 1)
        rows.add(i)
        j = i + 1
        while j < len(lines) and '|' in lines[j]:
            rows.add(j)
            j += 1
    offset = 0
    for i, line in enumerate(lines):
        if i in rows:
            blank_range(chars, offset, offset + len(line))
        offset += len(line) + 1


def mask_delimited_quotes(chars, open_ch, close_ch, apostrophe_aware=False):
    n = len(chars)

    def is_word(index):
        # JS reads chars[-1] and chars[n] as undefined, never a word char.
        return 0 <= index < n and bool(RE_ALNUM.search(chars[index]))

    def is_escaped(index):
        slashes = 0
        i = index - 1
        while i >= 0 and chars[i] == '\\':
            slashes += 1
            i -= 1
        return slashes % 2 == 1

    start = -1
    for i in range(n):
        if start == -1:
            if chars[i] == open_ch and not is_escaped(i) and (not apostrophe_aware or not is_word(i - 1)):
                start = i
        elif chars[i] == close_ch and not is_escaped(i) and (not apostrophe_aware or not is_word(i + 1)):
            blank_range(chars, start, i + 1)
            start = -1


def mask_hyphenation_protected(text):
    chars = list(mask_code(text))
    mask_top_level_indented_code(chars)
    mask_yaml_frontmatter(chars)
    mask_yaml_metadata(chars)
    mask_markdown_tables(chars)
    mask_delimited_quotes(chars, '"', '"')
    mask_delimited_quotes(chars, '“', '”')
    mask_delimited_quotes(chars, "'", "'", True)
    mask_delimited_quotes(chars, '‘', '’', True)
    for pattern in HYPHENATION_MASKS:
        source = ''.join(chars)
        for m in exec_all(js_re(*pattern), source):
            blank_range(chars, m.start(), m.end())
    return ''.join(chars)


def find_unnecessary_hyphenation(text):
    scan_text = mask_hyphenation_protected(text)
    issues = []
    for pattern, suggestion in UNNECESSARY_HYPHENATION:
        for m in exec_all(compile_js(pattern), scan_text):
            issues.append({
                'type': 'unnecessary-hyphenation',
                'text': m.group(0),
                'severity': 'medium',
                'suggestion': suggestion(m.group(0)) if callable(suggestion) else suggestion,
            })
    return issues


def is_social_tag(tag):
    return (not RE_DIGITS.search(tag) and not compile_js(HEX_COLOUR).search(tag)
            and not compile_js(CPP_DIRECTIVE).search(tag))


def count_separator_dashes(text):
    """(text.match(SEPARATOR_DASH_RE) || []).length without the backtracking.

    A match can start only at a line start p. The \\s* then has to stop at the
    end of the whitespace run that begins at p, because the rest of the
    pattern opens with a non-space character. So every line start inside one
    whitespace run succeeds or fails together, and the leftmost one is where
    JavaScript reports the match.
    """
    n = len(text)
    count = 0
    pos = 0
    while pos <= n:
        if pos == 0:
            p = 0
        else:
            lt = RE_LT.search(text, pos - 1)
            if lt is None:
                break
            p = lt.end()
        nw = RE_NOT_WS.search(text, p)
        run_end = nw.start() if nw else n
        m = RE_SEPARATOR_DASH_REST.match(text, run_end)
        if m:
            count += 1
            pos = m.end()
        else:
            pos = run_end + 1
    return count


def count_version_heading_dashes(value):
    count = 0
    for raw in RE_ANY_EOL_SPLIT.split(value):
        end = len(raw)
        while end > 0 and raw[end - 1] in ' \t':
            end -= 1
        if not RE_ISO_DATE.search(raw[max(0, end - 10):end]):
            continue
        cursor = end - 10
        while cursor > 0 and raw[cursor - 1] in ' \t':
            cursor -= 1
        # JS rawLine[-1] is undefined; guard instead of wrapping around.
        if cursor < 1 or raw[cursor - 1] != '—':
            continue
        cursor -= 1
        while cursor > 0 and raw[cursor - 1] in ' \t':
            cursor -= 1
        prefix = raw[:cursor]
        heading = compile_js(MD_HEADING_PREFIX).search(prefix)
        if not heading:
            continue
        version = prefix[len(heading.group(0)):]
        if version.startswith('['):
            if not version.endswith(']'):
                continue
            version = version[1:-1]
        elif version.endswith(']'):
            version = version[:-1]
        if ']' in version:
            continue
        if RE_SEMVER.search(version):
            count += 1
    return count


# ═══ Sentence regions + trinary classifier ═════════════════════════════════

def split_sentence_spans(text):
    spans = []
    length = len(text)
    pos = 0
    while pos < length:
        run = RE_TERMINATOR_RUN.search(text, pos)
        if run is None:
            head = RE_FIRST_NON_SPACE.search(text, pos)
            if head is not None:
                spans.append((head.start(), length))
            break
        if run.start() == pos:
            run_end = pos + len(run.group(0))
            if RE_TERMINATOR_RUN.search(text, run_end) is None:
                spans.append((run_end - 1, length))
                break
            pos = run_end
            continue
        end = run.end()
        spans.append((pos, end))
        pos = end
    return spans


def weight_of(issue_type):
    return ISSUE_WEIGHTS.get(issue_type, 2)


def build_sentence_regions(text, issues, trim_boundary_whitespace=False):
    sentences = []
    for span_start, span_end in split_sentence_spans(text):
        raw = text[span_start:span_end]
        sentence_text = js_trim(raw)
        if len(sentence_text) < 4:
            continue
        start, end = span_start, span_end
        if trim_boundary_whitespace:
            start += len(raw) - len(js_trim_start(raw))
            end -= len(raw) - len(js_trim_end(raw))
        sentences.append((start, end))
    if not sentences:
        return [], 0

    hits = [[0, 0] for _ in sentences]
    lower_text = js_lower(text)
    unmapped = 0
    for issue in issues:
        if not issue['text'] or len(issue['text']) > 200:
            continue
        if issue['type'] in NON_HIGHLIGHT_TYPES:
            continue
        w = weight_of(issue['type'])
        if w == 0:
            continue
        needle = js_lower(issue['text'])
        idx = 0
        matched = False
        while True:
            idx = lower_text.find(needle, idx)
            if idx == -1:
                break
            matched = True
            for i, (s, e) in enumerate(sentences):
                if s <= idx < e:
                    hits[i][0] += 1
                    hits[i][1] += w
                    break
            idx += len(needle)
        if not matched:
            unmapped += 1

    regions = []
    cur = None
    for i in range(len(sentences)):
        if hits[i][0] > 0:
            if cur is None:
                cur = {'startSentence': i, 'endSentence': i, 'start': sentences[i][0],
                       'end': sentences[i][1], 'hitCount': hits[i][0], 'weight': hits[i][1]}
            else:
                cur['endSentence'] = i
                cur['end'] = sentences[i][1]
                cur['hitCount'] += hits[i][0]
                cur['weight'] += hits[i][1]
        elif cur is not None:
            if i + 1 < len(hits) and hits[i + 1][0] > 0:
                cur['endSentence'] = i
                cur['end'] = sentences[i][1]
                continue
            regions.append(finalize_region(cur))
            cur = None
    if cur is not None:
        regions.append(finalize_region(cur))
    return regions, unmapped


def finalize_region(r):
    score = min(1, r['weight'] / 20)
    return {
        'startSentence': r['startSentence'],
        'endSentence': r['endSentence'],
        'start': r['start'],
        'end': r['end'],
        'hitCount': r['hitCount'],
        'score': js_round(score * 100) / 100,
    }


def classify_trinary(score, issues, norm_flags, word_count, dense_ai_vocab):
    types = set(i['type'] for i in issues)
    has_cutoff = 'cutoff-disclaimer' in types
    has_norm_flag = norm_flags['zeroWidth'] >= 2 or norm_flags['homoglyph'] >= 2
    strong = ((1 if has_cutoff else 0) + (1 if has_norm_flag else 0)
              + (1 if 'reasoning-artifact' in types and 'chatbot' in types else 0)
              + (1 if dense_ai_vocab else 0))
    stylometric = len([t for t in ('punct-distribution', 'cross-para-burstiness', 'fnword-trigram-entropy')
                       if t in types])
    weak = (1 if stylometric >= 2 else 0) + (1 if 'smart-punct-signature' in types else 0)
    total = strong + weak
    if score < 15 and strong == 0:
        classification = 'HUMAN_ONLY'
    elif strong >= 1 or score >= 70:
        classification = 'AI_ONLY'
    elif score >= 40 and total >= 1:
        classification = 'AI_ONLY'
    else:
        classification = 'MIXED'

    ai_soft = min(0.97, score / 100 + total * 0.06 + strong * 0.08)
    if classification == 'HUMAN_ONLY':
        p = [max(0.6, 1 - ai_soft), min(0.35, ai_soft * 0.8), min(0.1, ai_soft * 0.3)]
    elif classification == 'AI_ONLY':
        p = [max(0.02, 1 - ai_soft - 0.05), 0.1, ai_soft]
    else:
        p = [max(0.15, 0.6 - ai_soft * 0.5), 0.5, ai_soft * 0.7]
    raw_sum = p[0] + p[1] + p[2]
    human = float(js_to_fixed(p[0] / raw_sum, 3))
    mixed = float(js_to_fixed(p[1] / raw_sum, 3))
    ai = max(0, float(js_to_fixed(1 - human - mixed, 3)))
    probabilities = {'human': human, 'mixed': mixed, 'ai': ai}

    if strong >= 2 or has_cutoff or (score < 8 and word_count >= 100):
        confidence = 'high'
    elif strong >= 1 or (score >= 45 and weak >= 1) or score < 20:
        confidence = 'medium'
    else:
        confidence = 'low'
    return classification, probabilities, confidence


def get_label(score):
    if score == 0:
        return 'Clean'
    if score <= 15:
        return 'Minimal AI signals'
    if score <= 35:
        return 'Some AI patterns'
    if score <= 60:
        return 'Moderate AI signals'
    if score <= 80:
        return 'Strong AI signals'
    return 'Heavy AI patterns'


def get_color(score):
    if score <= 15:
        return '#44bb66'
    if score <= 35:
        return '#88bb44'
    if score <= 60:
        return '#ddaa00'
    if score <= 80:
        return '#ff8833'
    return '#ff4444'


def deduplicate_issues(issues):
    seen = set()
    out = []
    for issue in issues:
        key = issue['type'] + ':' + js_lower(issue['text'])
        if key in seen:
            continue
        seen.add(key)
        out.append(issue)
    return out


def _v2_defaults():
    return {
        'document_classification': 'UNSCORED',
        'class_probabilities': {'human': 0.333, 'mixed': 0.334, 'ai': 0.333},
        'confidence_category': 'low',
        'highlight_sentence_for_ai': [],
    }


# ═══ Main analysis ═════════════════════════════════════════════════════════

def analyze_u16(text, context_mode=None, source_mode=UNDEFINED):
    """analyzeText over a u16 string; returned strings are u16 strings too."""
    if not js_truthy(text) or len(js_trim(text)) == 0:
        result = _v2_defaults()
        result.update({'score': 0, 'label': 'Empty', 'issues': [], 'stats': {}, 'tooShort': True})
        return result

    source_map = list(range(len(text)))

    requested_mode = context_mode if js_truthy(context_mode) else 'general'
    mode = requested_mode if requested_mode in VALID_CONTEXT_MODES else 'general'
    mode_fallback = None if isinstance(requested_mode, str) and requested_mode == mode else requested_mode

    requested_source = 'plain' if source_mode is UNDEFINED else source_mode
    smode = requested_source if requested_source in VALID_SOURCE_MODES else 'plain'
    smode_fallback = UNDEFINED if isinstance(requested_source, str) and requested_source == smode else requested_source
    masked_frontmatter = 0
    masked_comments = 0
    rendered = smode == 'rendered-markdown'
    if rendered:
        text, masked_frontmatter, masked_comments = mask_rendered_markdown(text)

    if rendered:
        text, quoted_lines = mask_multiline_blockquotes(text)
    else:
        text, quoted_lines, source_map = strip_multiline_blockquotes(text, source_map)

    text, norm_flags, source_map = normalize_text(text, source_map)

    word_count = count_words(text)
    real = from_u16(text)
    cjk_chars = len(CJK_RE.findall(real))
    non_space = sum(1 for ch in real if ch not in JS_WS_CHARS)
    base_stats = [('wordCount', word_count), ('contextMode', mode), ('contextModeFallback', mode_fallback),
                  ('sourceMode', smode), ('sourceModeFallback', smode_fallback),
                  ('maskedFrontmatter', masked_frontmatter), ('maskedHtmlComments', masked_comments)]
    if cjk_chars > 0 and cjk_chars * 2 >= non_space:
        stats = dict(base_stats[:1])
        stats['cjkChars'] = cjk_chars
        stats['reason'] = 'unsegmented-script document: no inter-word spaces to count'
        stats.update(base_stats[1:])
        result = _v2_defaults()
        result.update({'score': 0, 'label': 'Unsupported script', 'issues': [], 'stats': stats,
                       'unsupportedScript': True})
        return result
    if word_count < 10 or word_count > MAX_WORDS:
        result = _v2_defaults()
        result.update({'score': 0, 'label': 'Too short' if word_count < 10 else 'Text too long',
                       'issues': [], 'stats': dict(base_stats)})
        result['tooShort' if word_count < 10 else 'tooLong'] = True
        return result

    tokens = tokenize(text)
    paragraphs = get_paragraphs(text)
    sentences = get_sentences(text)
    technical = mode == 'technical'
    issues = []

    # ── 1. Tier 1 words and phrases ──
    tier1_found = set()
    for token in tokens:
        if technical and token in TECHNICAL_EXEMPT:
            continue
        if token in TIER1 and token not in tier1_found:
            tier1_found.add(token)
            issues.append({'type': 'tier1', 'text': token, 'severity': 'high', 'suggestion': TIER1[token]})
    for pattern, replace, clarity in TIER1_PHRASES:
        for m in exec_all(compile_js(pattern), text):
            lower = js_lower(m.group(0))
            if technical and lower in TECHNICAL_EXEMPT:
                continue
            if lower in tier1_found:
                continue
            tier1_found.add(lower)
            issues.append({
                'type': 'tier1-clarity' if clarity else 'tier1',
                'text': m.group(0),
                'severity': 'medium' if clarity else 'high',
                'suggestion': replace,
            })

    # ── 2. Tier 2 clusters ──
    tier2_clusters = 0
    for para in paragraphs:
        found = []
        suggestions = {}
        for token in tokenize(para):
            if technical and token in TECHNICAL_EXEMPT:
                continue
            if token in TIER2 and token not in found:
                found.append(token)
                suggestions[token] = TIER2[token]
        for word, pattern, suggestion in TIER2_CONDITIONAL:
            if technical and word in TECHNICAL_EXEMPT:
                continue
            if word not in found and compile_js(pattern).search(para):
                found.append(word)
                suggestions[word] = suggestion
        if len(found) >= 2:
            tier2_clusters += 1
            for word in found:
                issues.append({'type': 'tier2', 'text': word, 'severity': 'medium', 'suggestion': suggestions[word]})

    # ── 3. Tier 3 density ──
    tier3_counts = {}
    for token in tokens:
        canonical = TIER3_LOOKUP.get(token)
        if canonical:
            tier3_counts[canonical] = tier3_counts.get(canonical, 0) + 1
    density_threshold = max(3, int(math.floor(word_count * 0.03)))
    tier3_flags = 0
    for word, count in tier3_counts.items():
        if count >= density_threshold:
            tier3_flags += 1
            issues.append({
                'type': 'tier3',
                'text': '"%s" x%d' % (word, count),
                'severity': 'low',
                'suggestion': 'Overused (%d times in %d words)' % (count, word_count),
            })

    # ── 4-21. Pattern categories ──
    issues += match_patterns(text, TRANSITIONS, 'transition', 'medium')
    issues += match_patterns(text, CHATBOT_ARTIFACTS, 'chatbot', 'critical')
    issues += match_patterns(text, SYCOPHANTIC, 'sycophantic', 'critical')
    issues += match_patterns(text, FILLERS, 'filler', 'medium')
    issues += match_patterns(text, GENERIC_CONCLUSIONS, 'generic-conclusion', 'medium')
    issues += match_patterns(text, LETS_PATTERNS, 'lets-construction', 'medium')
    issues += match_patterns(text, REASONING_ARTIFACTS, 'reasoning-artifact', 'critical')
    issues += match_patterns(text, SIGNIFICANCE_INFLATION, 'significance-inflation', 'high')
    issues += match_patterns(text, VAGUE_ATTRIBUTIONS, 'vague-attribution', 'critical')
    issues += match_patterns(text, HOLLOW_INTENSIFIERS, 'hollow-intensifier', 'medium')
    issues += match_patterns(text, EMOTIONAL_FLATLINE, 'emotional-flatline', 'low')
    issues += match_patterns(text, LINGERING_ATTENTION, 'lingering-attention', 'medium')
    issues += match_patterns(text, NOVELTY_INFLATION, 'novelty-inflation', 'medium')
    issues += match_patterns(text, CUTOFF_DISCLAIMERS, 'cutoff-disclaimer', 'critical')
    issues += match_patterns(text, AI_PLACEHOLDERS, 'ai-placeholder', 'critical')
    issues += match_patterns(text, AI_CITATION_MARKUP, 'ai-citation-markup', 'critical')
    issues += match_patterns(text, AI_UTM_SOURCE, 'ai-utm-source', 'critical')
    issues += match_patterns(text, TEMPLATE_PHRASES, 'template-phrase', 'high')
    issues += match_patterns(text, FALSE_CONCESSION, 'false-concession', 'medium')
    issues += match_patterns(text, RHETORICAL_QUESTIONS, 'rhetorical-question', 'medium')
    issues += match_patterns(text, HEDGE_STACK, 'hedge-stack', 'high')
    issues += match_patterns(text, FUTURE_NARRATIVE, 'future-narrative', 'high')
    issues += match_patterns(text, REAL_ACTUAL_INFLATION, 'real-actual-inflation', 'medium')
    issues += match_patterns(text, SOCIAL_CTA_CLOSER, 'social-cta-closer', 'high')
    issues += match_patterns(text, PERFORMED_INSIGHT, 'performed-insight', 'medium')
    staged = match_patterns(text, STAGED_DISCOVERY, 'performed-insight', 'medium')
    issues += staged
    issues += match_patterns(text, NEGATION_CHAIN, 'negation-chain', 'high')
    issues += match_patterns(text, DEV_BLOG_BOILERPLATE, 'dev-blog-boilerplate', 'medium')
    issues += find_unnecessary_hyphenation(text)

    issues += match_patterns(text, FORMULAIC_OPENERS, 'formulaic-opener', 'high')
    issues += match_patterns(text, SPECULATIVE_OPENERS, 'speculative-opener', 'high')
    issues += match_patterns(text, LAUNCH_INTROS, 'launch-intro', 'high')
    issues += match_patterns(text, CROWD_CONTRAST, 'crowd-contrast', 'medium')
    issues += match_patterns(text, FAKE_CASUAL_PROPS, 'fake-casual-prop', 'high')
    issues += match_patterns(text, PARENTHETICAL_HEDGE, 'parenthetical-hedge', 'medium')

    # Title-case headers (skipped in technical mode).
    if not technical:
        title_hits = match_patterns(text, [TITLE_CASE_HEADER], 'title-case-header', 'medium')
        prefix_re = compile_js(MD_HEADING_PREFIX)
        function_word = compile_js(FUNCTION_WORD)
        ws_split = py_re(WS + '+')
        filtered = []
        for h in title_hits:
            title = prefix_re.sub('', h['text'], count=1)
            words = ws_split.split(js_trim(title))
            if len(words) < 4:
                continue
            if function_word.search(' '.join(words[1:])):
                filtered.append(h)
        fences = fence_ranges(text) if filtered else []
        issues += [h for h in filtered if not in_fence_range(fences, h['index'])]

    # Normalization-trigger flag.
    if norm_flags['zeroWidth'] > 0 or norm_flags['homoglyph'] >= 2:
        issues.append({
            'type': 'normalization-flag',
            'text': '%d zero-width + %d homoglyph swap%s' % (
                norm_flags['zeroWidth'], norm_flags['homoglyph'], '' if norm_flags['homoglyph'] == 1 else 's'),
            'severity': 'critical',
            'suggestion': 'Text contains invisible/lookalike chars typical of AI-humanizer bypass tools. Re-type from your own keyboard.',
        })
    if norm_flags['roleplay'] >= 2:
        issues.append({
            'type': 'normalization-flag',
            'text': '%d *roleplay-action* markers stripped' % norm_flags['roleplay'],
            'severity': 'high',
            'suggestion': 'Paired *action* markers are a chat-model artifact.',
        })

    # Smart-punctuation co-occurrence signature.
    separator_dashes = count_separator_dashes(text) + count_version_heading_dashes(text)
    has_curly = bool(RE_CURLY.search(text))
    has_em_dash = text.count('—') > separator_dashes
    has_oxford = len(exec_all(RE_OXFORD, text)) >= 1
    double_spaces = len(exec_all(RE_DOUBLE_SPACE, text))
    missing_apos = bool(RE_MISSING_APOS.search(text))
    clean = double_spaces == 0 and not missing_apos
    if has_curly and has_em_dash and has_oxford and clean and word_count >= 80:
        issues.append({
            'type': 'smart-punct-signature',
            'text': 'curly-quotes + em-dash + Oxford comma + zero typos',
            'severity': 'high',
            'suggestion': 'Smart-punctuation signature consistent with LLM output. Humans typing into textareas rarely produce all four.',
        })

    # Punctuation distribution.
    if len(paragraphs) >= 4:
        densities = []
        for p in paragraphs:
            words = count_words(p)
            if words < 5:
                continue
            densities.append(len(exec_all(RE_PUNCT, p)) / words)
        if len(densities) >= 4:
            mean = _fsum(densities) / len(densities)
            variance = _fsum((d - mean) ** 2 for d in densities) / len(densities)
            cv = math.sqrt(variance) / mean if mean > 0 else 0
            if cv < 0.25 and mean >= 0.04:
                issues.append({
                    'type': 'punct-distribution',
                    'text': 'Punctuation density uniform across paragraphs (CV=%s)' % js_to_fixed(cv, 2),
                    'severity': 'medium',
                    'suggestion': 'AI text holds punctuation density steady; human writers swing between dense and sparse paragraphs.',
                })

    # Function-word trigram entropy.
    if word_count >= 150:
        mapped = [t if t in FUNC_WORDS else '_' for t in tokens]
        seq = [t for i, t in enumerate(mapped) if t != '_' or (i > 0 and mapped[i - 1] != '_')]
        if len(seq) >= 50:
            trigrams = {}
            for i in range(len(seq) - 2):
                tg = seq[i] + '|' + seq[i + 1] + '|' + seq[i + 2]
                trigrams[tg] = trigrams.get(tg, 0) + 1
            total = len(seq) - 2
            entropy = 0
            for c in trigrams.values():
                p = c / total
                entropy -= p * math.log2(p)
            distinct = len(trigrams)
            normalized = entropy / math.log2(distinct) if distinct > 1 else 1
            if normalized < 0.82 and total >= 50:
                issues.append({
                    'type': 'fnword-trigram-entropy',
                    'text': 'Function-word trigram entropy %s (low)' % js_to_fixed(normalized, 2),
                    'severity': 'medium',
                    'suggestion': 'Grammatical structure is unusually repetitive. AI sampling collapses onto narrower templates than human writing.',
                })
            if distinct == 1 and total >= 50:
                issues.append({
                    'type': 'fnword-trigram-entropy',
                    'text': 'Single function-word trigram repeated across document',
                    'severity': 'high',
                    'suggestion': 'Grammatical structure is fully degenerate — every clause uses the same function-word skeleton.',
                })

    # Cross-paragraph burstiness.
    if len(paragraphs) >= 4:
        cvs = []
        for p in paragraphs:
            sents = get_sentences(p)
            if len(sents) < 3:
                continue
            lens = [count_words(s) for s in sents]
            m = _fsum(lens) / len(lens)
            if m == 0:
                continue
            v = _fsum((l - m) ** 2 for l in lens) / len(lens)
            cvs.append(math.sqrt(v) / m)
        if len(cvs) >= 4:
            cv_mean = _fsum(cvs) / len(cvs)
            cv_var = _fsum((c - cv_mean) ** 2 for c in cvs) / len(cvs)
            cv_std = math.sqrt(cv_var)
            if cv_std < 0.08 and cv_mean < 0.45:
                issues.append({
                    'type': 'cross-para-burstiness',
                    'text': 'Sentence-rhythm uniform across paragraphs (σCV=%s)' % js_to_fixed(cv_std, 2),
                    'severity': 'medium',
                    'suggestion': 'Every paragraph has the same internal rhythm. Humans vary cadence between terse and discursive paragraphs.',
                })

    # Tier 3 multi-word phrases.
    claimed = []
    distinct_phrases = 0
    for pattern in TIER3_PHRASES:
        phrase_spans = []
        for m in exec_all(compile_js(pattern), text):
            s, e = m.start(), m.end()
            if not any(s < ce and e > cs for cs, ce in claimed):
                phrase_spans.append((s, e, m.group(0)))
        if not phrase_spans:
            continue
        claimed.extend((s, e) for s, e, _ in phrase_spans)
        distinct_phrases += 1
        if len(phrase_spans) >= 2:
            n = len(phrase_spans)
            issues.append({
                'type': 'tier3-phrase',
                'text': '"%s" x%d' % (js_lower(phrase_spans[0][2]), n),
                'severity': 'medium',
                'suggestion': 'Boilerplate phrase repeated %d× — replace at least one with specifics' % n,
            })
    if distinct_phrases >= 3:
        issues.append({
            'type': 'tier3-phrase-cluster',
            'text': '%d distinct boilerplate phrases' % distinct_phrases,
            'severity': 'high',
            'suggestion': 'Several stock crypto/web3 phrases stacked in one piece. Rewrite around one specific claim or observation.',
        })

    # Hashtag stuffing.
    hashtags = [m for m in exec_all(RE_HASHTAG, mask_code(text)) if is_social_tag(m.group(1))]
    if len(hashtags) >= 6:
        issues.append({
            'type': 'hashtag-stuff',
            'text': '%d hashtags' % len(hashtags),
            'severity': 'medium',
            'suggestion': 'Cut to 2-3 specific tags or none. Long hashtag blocks read as bot output.',
        })

    # Bullet list of bare noun phrases.
    def parse_bullet(line):
        cursor = 0
        n = len(line)
        while cursor < n and line[cursor] in JS_WS_CHARS:
            cursor += 1
        if cursor >= n or line[cursor] not in ('*', '-', '•', '+'):
            return None
        cursor += 1
        spacing_start = cursor
        while cursor < n and line[cursor] in JS_WS_CHARS:
            cursor += 1
        if cursor == spacing_start:
            return None
        if cursor >= n:
            return '' if cursor - spacing_start >= 2 else None
        return js_trim(line[cursor:])

    state = {'run': [], 'blank': 0}

    def flush_run():
        run = state['run']
        if len(run) >= 5:
            bare_np = [it for it in run if 0 < count_words(it) <= 6 and not RE_VERB.search(it)]
            if len(bare_np) >= 5 and len(bare_np) / len(run) >= 0.75:
                issues.append({
                    'type': 'bullet-np-list',
                    'text': '%d-item bullet list of bare noun phrases' % len(run),
                    'severity': 'high',
                    'suggestion': 'Convert to a prose paragraph or merge items. Long lists of bare adj+noun pairs read as AI scaffolding.',
                })
        state['run'] = []
        state['blank'] = 0

    in_fence = False
    for line in RE_CRLF_SPLIT.split(text):
        if RE_BULLET_FENCE.search(line):
            flush_run()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        bullet = parse_bullet(line)
        if bullet is not None:
            state['run'].append(bullet)
            state['blank'] = 0
        elif js_trim(line) == '':
            state['blank'] += 1
            if state['blank'] >= 2:
                flush_run()
        else:
            flush_run()
    flush_run()

    # Confidence calibration: only when it stacks (3+ raw matches).
    conf = match_patterns(text, CONFIDENCE_CALIBRATION, 'confidence-calibration', 'low')
    if len(conf) >= 3:
        issues += conf

    # ── 22. Em dash frequency ──
    em_dash_count = len(exec_all(EM_DASH_RE, text)) - separator_dashes
    if em_dash_count / (word_count / 1000) > 1:
        issues.append({
            'type': 'em-dash',
            'text': '%d em dashes in %d words' % (em_dash_count, word_count),
            'severity': 'medium',
            'suggestion': 'Replace with commas, periods, or rewrite',
        })

    # ── 23. Sentence length uniformity ──
    if len(sentences) >= 5:
        lengths = [count_words(s) for s in sentences]
        avg = _fsum(lengths) / len(lengths)
        variance = _fsum((l - avg) ** 2 for l in lengths) / len(lengths)
        cv = math.sqrt(variance) / avg if avg > 0 else 0
        if cv < 0.25 and avg > 10:
            issues.append({
                'type': 'uniformity',
                'text': 'Sentence lengths cluster around %d words (low variation)' % js_round(avg),
                'severity': 'medium',
                'suggestion': 'Mix short punchy sentences with longer flowing ones',
            })

    # Type-token ratio.
    if len(tokens) >= 200:
        unique = len(set(tokens))
        ttr = unique / len(tokens)
        if ttr < 0.4:
            issues.append({
                'type': 'low-ttr',
                'text': 'Vocabulary diversity %s%% (%d unique / %d tokens)' % (js_to_fixed(ttr * 100, 1), unique, len(tokens)),
                'severity': 'low',
                'suggestion': 'Text reuses a narrow word set. Vary nouns and verbs deliberately, or check if the topic genuinely warrants the repetition.',
            })

    # ── 24. Paragraph length uniformity ──
    if len(paragraphs) >= 4:
        para_lengths = [len(get_sentences(p)) for p in paragraphs]
        avg = _fsum(para_lengths) / len(para_lengths)
        if all(abs(l - avg) <= 1 for l in para_lengths) and avg >= 3:
            issues.append({
                'type': 'uniformity',
                'text': 'All paragraphs are ~%d sentences' % js_round(avg),
                'severity': 'low',
                'suggestion': 'Vary paragraph length deliberately',
            })

    # ── 25. Bold overuse ──
    bold = len(exec_all(RE_BOLD, text))
    if bold > 3:
        issues.append({
            'type': 'formatting',
            'text': '%d bold phrases' % bold,
            'severity': 'medium',
            'suggestion': 'Strip bold from most; restructure to lead with key info',
        })

    # ── Score from the deduped issue list ──
    staged_ids = set(id(i) for i in staged)
    staged_spans = [(i['index'], i['index'] + len(i['text'])) for i in staged]
    kept = []
    for issue in issues:
        if (issue['type'] not in ('emotional-flatline', 'performed-insight') or id(issue) in staged_ids
                or 'index' not in issue
                or not any(issue['index'] >= s and issue['index'] + len(issue['text']) <= e for s, e in staged_spans)):
            kept.append(issue)
    deduped = deduplicate_issues(kept)
    raw_score = _fsum(weight_of(i['type']) for i in deduped)

    length_factor = max(1, math.log2(word_count / 50))
    score = min(100, js_round(raw_score / length_factor))
    label = get_label(score)

    regions, unmapped = build_sentence_regions(text, deduped, rendered)

    tier1_count = sum(1 for i in deduped if i['type'] == 'tier1')
    tier2_count = sum(1 for i in deduped if i['type'] == 'tier2')
    tier3_count = sum(1 for i in deduped if i['type'] == 'tier3')
    tier1_distinct = len(set(js_lower(i['text'] or '') for i in deduped if i['type'] == 'tier1'))
    has_transition = any(i['type'] == 'transition' for i in deduped)
    dense_ai_vocab = word_count >= 150 and tier1_distinct >= 5 and tier2_clusters >= 2 and has_transition

    classification, probabilities, confidence = classify_trinary(
        score, deduped, norm_flags, word_count, dense_ai_vocab)

    # Translate issue indexes and half-open region bounds to source offsets.
    for issue in deduped:
        if 'index' in issue:
            issue['index'] = source_map[issue['index']]
    for region in regions:
        region['start'] = source_map[region['start']]
        region['end'] = source_map[region['end'] - 1] + 1

    return {
        'score': score,
        'label': label,
        'issues': deduped,
        'stats': {
            'wordCount': word_count,
            'tier1Count': tier1_count,
            'tier2Count': tier2_count,
            'tier2Clusters': tier2_clusters,
            'tier3Count': tier3_count,
            'tier3Flags': tier3_flags,
            'patternCount': len(deduped) - tier1_count - tier2_count - tier3_count,
            'contextMode': mode,
            'contextModeFallback': mode_fallback,
            'sourceMode': smode,
            'sourceModeFallback': smode_fallback,
            'maskedFrontmatter': masked_frontmatter,
            'maskedHtmlComments': masked_comments,
            'normalization': norm_flags,
            'quotedLines': quoted_lines,
            'unmappedHighlights': unmapped,
            'denseAIVocab': dense_ai_vocab,
            'tier1Distinct': tier1_distinct,
        },
        'document_classification': classification,
        'class_probabilities': probabilities,
        'confidence_category': confidence,
        'highlight_sentence_for_ai': regions,
    }


def _to_python_strings(value):
    if isinstance(value, str):
        return from_u16(value)
    if isinstance(value, list):
        return [_to_python_strings(v) for v in value]
    if isinstance(value, dict):
        return dict((k, _to_python_strings(v)) for k, v in value.items())
    return value


def analyze_text(text, context_mode=None, source_mode=UNDEFINED):
    """Port of AIDetector.analyzeText(text, {contextMode, sourceMode}).

    context_mode: 'general' (default), 'technical', 'marketing', 'personal'.
    source_mode: 'plain' (default) or 'rendered-markdown'.
    Invalid values fall back as in JavaScript and are reported in stats.
    Returns the result dict; stats['sourceModeFallback'] is UNDEFINED (and
    omitted from JSON) unless a fallback happened.
    """
    if isinstance(text, str):
        text = to_u16(text)
    return _to_python_strings(analyze_u16(text, context_mode, source_mode))


def to_json(result):
    """JSON.stringify(result, null, 2)."""
    return js_stringify(result, 2)


# ═══ CLI (bin/avoid-ai-writing.js) ═════════════════════════════════════════

USAGE = """Usage: avoid-ai-writing [options] [file]

Scores UTF-8 text from a file path or stdin and prints the complete
analyzeText() result as JSON to stdout. Read-only: nothing is modified.
Exits 0 after a successful analysis, 2 on usage or I/O errors.

Options:
  --context <general|technical|marketing|personal>
                                         Analysis context (default: general)
  --source-mode <plain|rendered-markdown>
                                         Plain text (default) or rendered
                                         Markdown, which excludes YAML
                                         frontmatter and HTML comments from
                                         the score
  -h, --help                             Show this help

Use "--" to stop option parsing when the file name starts with a dash.

Examples:
  npx --package avoid-ai-writing-detector avoid-ai-writing draft.md
  cat draft.md | npx --package avoid-ai-writing-detector avoid-ai-writing --context technical
  npx --package avoid-ai-writing-detector avoid-ai-writing --source-mode rendered-markdown -- --draft.md
"""

CONTEXTS = ['general', 'technical', 'marketing', 'personal']
SOURCE_MODES = ['plain', 'rendered-markdown']


def parse_args(argv):
    options = {'help': False, 'context': 'general', 'sourceMode': 'plain', 'files': []}
    end_of_options = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if end_of_options:
            options['files'].append(arg)
        elif arg == '--':
            end_of_options = True
        elif arg in ('-h', '--help'):
            options['help'] = True
        elif arg in ('--context', '--source-mode'):
            if i + 1 >= len(argv):
                return {'error': '%s requires a value' % arg}
            value = argv[i + 1]
            i += 1
            if arg == '--context':
                if value not in CONTEXTS:
                    return {'error': 'invalid --context value: %s' % value}
                options['context'] = value
            else:
                if value not in SOURCE_MODES:
                    return {'error': 'invalid --source-mode value: %s' % value}
                options['sourceMode'] = value
        elif arg.startswith('-') and arg != '-':
            return {'error': 'unknown option: %s' % arg}
        else:
            options['files'].append(arg)
        i += 1
    if len(options['files']) > 1:
        return {'error': 'expected at most one file path'}
    return options


def read_input_fatal(path, label):
    """Read bytes and decode like TextDecoder('utf-8', {fatal: true}) (BOM stripped)."""
    try:
        if path is None:
            data = sys.stdin.buffer.read()
        else:
            with open(path, 'rb') as fh:
                data = fh.read()
    except OSError as exc:
        return None, 'cannot read %s: %s' % (label, node_fs_error(exc, path))
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return None, 'cannot read %s: input is not valid UTF-8' % label
    if text.startswith('﻿'):
        text = text[1:]
    return to_u16(text), None


def main(argv):
    parsed = parse_args(argv)
    if 'error' in parsed:
        write_stderr('avoid-ai-writing: %s\n\n%s' % (parsed['error'], USAGE))
        return 2
    if parsed['help']:
        write_stdout(USAGE)
        return 0
    file = parsed['files'][0] if parsed['files'] else None
    from_stdin = file is None or file == '-'
    text, error = read_input_fatal(None if from_stdin else file, 'stdin' if from_stdin else file)
    if error:
        write_stderr('avoid-ai-writing: %s\n\n%s' % (error, USAGE))
        return 2
    result = analyze_u16(text, parsed['context'], parsed['sourceMode'])
    if result.get('stats') == {}:
        result['stats']['contextMode'] = parsed['context']
        result['stats']['sourceMode'] = parsed['sourceMode']
    write_stdout(js_stringify(result, 2) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
