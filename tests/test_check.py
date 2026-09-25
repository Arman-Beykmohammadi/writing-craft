"""Tests for scripts/check.py. Run: python3 -m unittest discover -s tests -p 'test_*.py'

All sample sentences are invented.
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))

import check  # noqa: E402

# (entry, language, sample that must fire it with no genre settings)
POSITIVE = [
    ("F1", "en", "Our platform now serves hundreds of users across the region."),
    ("F3", "en", "Dear [Your Name], thank you for the call on 2026-XX-XX."),
    ("F3", "de", "Sehr geehrte Frau Mustermann, Max Mustermann aus der Musterstraße 1."),
    ("F4", "en", "Experts believe this approach will define the next decade."),
    ("F4", "de", "Studien belegen, dass dieses Verfahren besser ist."),
    ("F5", "en", "As of my last update, the company had not announced a successor."),
    ("F5", "de", "Soweit mir bekannt ist, gibt es dazu keine Angaben."),
    ("C1", "en", "Certainly! Here is a revised version of your paragraph."),
    ("C1", "de", "Ich hoffe, das hilft dir bei deiner Bewerbung weiter."),
    ("C2", "en", "Great question! The answer depends on the setup."),
    ("C2", "de", "Tolle Frage! Das hängt vom Aufbau ab."),
    ("C4", "en", "Let me think step by step about the migration plan."),
    ("C5", "en", "See the notes at https://example.org/a?utm_source=chatgpt.com for details."),
    ("I1", "en", "The launch marked a pivotal moment in the evolution of the city's transit."),
    ("I1", "de", "Datenschutz spielt in unserem Team eine entscheidende Rolle."),
    ("I2", "en", "The future looks bright for the whole team."),
    ("I2", "de", "Die Zukunft sieht rosig aus für unser Projekt."),
    ("I3", "en", "Nestled in the heart of the valley, the clinic offers breathtaking views."),
    ("I3", "de", "Eingebettet im Herzen der Altstadt liegt unser atemberaubend schönes Büro."),
    ("I4", "en", "We delve into the tapestry of modern logistics."),
    ("I4", "de", "Das Konzept schafft Synergien und einen Paradigmenwechsel."),
    ("I6", "en", "The team moved to weekly releases, highlighting its commitment to speed."),
    ("I6", "de", "Das Team veröffentlicht jede Woche und unterstreicht damit seinen Anspruch."),
    ("I7", "en", "This is the failure mode nobody's naming in data teams."),
    ("I8", "en", "This is genuinely hard, and truly worth the effort."),
    ("I9", "en", "We finally have real adoption among the pilot sites."),
    ("I10", "en", "The chart gives an honest shape to the data."),
    ("I11", "de", "Der Bericht steht in Verbindung zu den Zahlen vom Vorjahr."),
    ("I12", "en", "The library serves as the main archive for the region."),
    ("I12", "de", "Der Raum dient als Treffpunkt für das Team."),
    ("S1", "en", "It's not just a dashboard, it's a new way of working."),
    ("S1", "de", "Es geht nicht um Geschwindigkeit, sondern um Verlässlichkeit."),
    ("S3", "en", "No meetings, no status reports, no busywork on Fridays."),
    ("S4", "en", "Read that again. Every. Single. Day."),
    ("S6", "en", "At its core, trust is the currency of teamwork."),
    ("S6", "de", "Im Kern geht es um Vertrauen im Team."),
    ("S7", "en", "Let's dive in. Here's what you need to know about caching."),
    ("S7", "de", "Tauchen wir ein in die Welt der Logistik."),
    ("S8", "en", "The catch? It only works on weekends."),
    ("S9", "en", "Let that sink in for a second."),
    ("S10", "en", "Don't get me wrong, I like the old system."),
    ("S11", "en", "While automation is impressive, trust remains a challenge."),
    ("S12", "en", "But what does this mean for developers?"),
    ("S13", "en", "In today's fast-paced world, every team needs a data strategy."),
    ("S13", "de", "In der heutigen Zeit braucht jedes Team eine Datenstrategie."),
    ("S14", "en", "I'm thrilled to share that our paper was accepted."),
    ("S14", "de", "Mit großer Begeisterung habe ich Ihre Anzeige gelesen."),
    ("S15", "en", "This one is worth your time: a long read on caching."),
    ("S16", "en", "Meet Ledgerly, your new favorite budgeting app."),
    ("S17", "en", "Fixed the bug on the first try *chef's kiss*"),
    ("S18", "en", "That last step is the contrarian one."),
    ("S21", "en", "Whether you're a founder or an engineer, this guide helps."),
    ("S22", "en", "Install it and it just works with sane defaults."),
    ("S23", "en", "The implications are significant for every city."),
    ("R2", "en", "The change could potentially reduce costs."),
    ("R2", "de", "Die Änderung könnte möglicherweise Kosten sparen."),
    ("R2", "en", "Longer shifts may suggest that sleep quality is associated with wellbeing."),
    ("R2", "de", "Die Daten könnten darauf hindeuten, dass die Legierung besser ist."),
    ("S13", "de", "Künstliche Intelligenz gewinnt in der Logistik, insbesondere bei der Tourenplanung, zunehmend an Bedeutung."),
    ("G4", "de", "Ich freue mich auf Ihre Antwort.\n\nMit freundlichen Grüßen,\nLea Brandt"),
    ("R3", "en", "The tool helps analysts (and, increasingly, managers) plan budgets."),
    ("R5", "en", "It is important to note that the budget is fixed."),
    ("R5", "de", "Es ist wichtig zu betonen, dass das Budget feststeht."),
    ("R6", "en", "The plan — approved last week — starts now."),
    ("R6", "de", "Der Plan — letzte Woche beschlossen — startet jetzt."),
    ("R17", "en", "The code-base is updated in real-time."),
    ("R18", "de", "Die Durchführung der Optimierung der Gestaltung der Abläufe erfolgte zügig."),
    ("M4", "en", "Proud of the team! #AI #Data #Innovation #Growth #Tech #Future #Leadership"),
    ("G1", "de", "Wir müssen mehr performen, die Learnings teilen und das Mindset ändern."),
    ("G2", "de", "Das macht Sinn, weil wir in 2024 gewachsen sind."),
    ("G4", "de", "Sehr geehrte Frau Keller, ich danke Ihnen. Du weißt ja, wie das ist."),
]

# Ordinary text that must stay free of the named entries.
NEGATIVE = [
    ("R6", "de", "prose", "blog", "Nach drei Jahren wechsle ich ins Controlling – intern, gleiches Team."),
    ("C1", "de", "prose", "email", "Gerne sende ich Ihnen die Unterlagen bis Freitag zu."),
    ("R10", "en", "science", "methods", "Samples were centrifuged and stored at -80 °C. Cortisol was measured by ELISA."),
    ("S4", "en", "cv", "default", "- Built the tracking API in Python\n- Wrote SQL checks\n- On call one week per month"),
    ("R4", "de", "prose", "blog", "Dabei zeigte sich, dass der Plan funktioniert. Gleichzeitig blieb das Budget stabil."),
    ("S1", "de", "prose", "blog", "Das Angebot gilt nicht nur in Berlin, sondern auch in Wien."),
    ("F5", "de", "cv", "default", "Stand: 09/2026"),
    ("I8", "de", "prose", "linkedin", "Ehrlich gesagt hatte ich ja ein bisschen Bammel, aber das Team war super."),
    ("G4", "de", "prose", "letter", "Ich freue mich auf Ihre Antwort.\n\nMit freundlichen Grüßen\nLea Brandt"),
]


def ids(result):
    return {f["id"] for f in result["findings"]}


class MarkerTests(unittest.TestCase):
    def test_catalog_parses(self):
        entries = check.parse_catalog()
        self.assertEqual(len(entries), 75)
        for entry in entries.values():
            self.assertIn(entry.tier, ("F", "P0", "P1", "P2"), entry.id)

    def test_positive_samples(self):
        for eid, lang, sample in POSITIVE:
            with self.subTest(entry=eid, lang=lang):
                result = check.scan(sample, lang=lang, genre=None)
                raw = check.scan(sample + "\n\nFiller paragraph one.\n\nFiller two.", lang=lang)
                self.assertTrue(eid in ids(result) or eid in ids(raw) or self._fires_raw(eid, lang, sample),
                                "%s did not fire on: %s" % (eid, sample))

    def _fires_raw(self, eid, lang, sample):
        entry = check.parse_catalog()[eid]
        return any(regex.search(check.mask_protected(sample)) for regex, _, _ in entry.checks[lang])

    def test_negative_samples(self):
        for eid, lang, genre, section, sample in NEGATIVE:
            with self.subTest(entry=eid, genre=genre, section=section):
                result = check.scan(sample, genre=genre, column=section, lang=lang)
                self.assertNotIn(eid, ids(result), "%s fired on ordinary text: %s" % (eid, sample))

    def test_settings_off_suppresses(self):
        text = "Participants were recruited. Consent was obtained. Samples were stored."
        result = check.scan(text, genre="science", column="methods", lang="en")
        self.assertNotIn("R10", ids(result))


class FactTests(unittest.TestCase):
    SOURCE = ("Data team, Halden Logistics, 03/2021 - 06/2023\n"
              "- contributed to moving the nightly reports to Airflow\n"
              "- finalist, internal hackathon 2022\nPhone: +49 30 1234567\n"
              "Revenue 12,500 EUR; response time 1.5 s; see https://example.org/x?run=7\n")

    def facts(self, output, lang="en", genre="cv"):
        return check.scan(output, genre=genre, lang=lang, source=self.SOURCE)["findings"]

    def test_invented_number_flagged(self):
        found = [f for f in self.facts("- Cut report time by 40% using Airflow") if f["id"] == "F1"]
        self.assertTrue(any("40" in f["text"] for f in found))

    def test_same_facts_in_other_formats_pass(self):
        output = ("Halden Logistics, Mar 2021 – Jun 2023. Phone 030 1234567. "
                  "Revenue 12.500 EUR, response time 1,5 s, https://example.org/x?run=7. Hackathon 2022.")
        self.assertEqual([f for f in self.facts(output) if f["id"] == "F1"], [])

    def test_date_not_in_source(self):
        found = self.facts("Available from 15 March 2027.")
        self.assertTrue(any(f["id"] == "F1" and "2027" in f["text"] for f in found))

    def test_changed_url_flagged(self):
        found = self.facts("Details: https://example.org/x?run=8")
        self.assertTrue(any(f["id"] == "F1" and "run=8" in f["text"] for f in found))

    def test_ai_tracking_parameter_ignored(self):
        found = self.facts("Details: https://example.org/x?run=7&utm_source=chatgpt.com")
        self.assertFalse(any(f["id"] == "F1" and "example.org" in f["text"] for f in found))

    def test_ladder_upgrade_flagged(self):
        found = self.facts("- Led the move of nightly reports to Airflow\n- Winner, internal hackathon 2022")
        words = {f["text"].lower() for f in found if f["id"] == "F2"}
        self.assertIn("led", words)
        self.assertIn("winner", words)

    def test_german_ladder_upgrade_flagged(self):
        source = "2023 Finalist, Hochschul-Hackathon"
        result = check.scan("2023 Gewinner, Hochschul-Hackathon", genre="cv", lang="de", source=source)
        self.assertIn("F2", ids(result))

    def test_number_qualifier_changes(self):
        source = "Verfügbar ab 01.11.2026, 20 Stunden pro Woche. Abstimmung von rund 400 Rechnungen."
        output = "Ab dem 01.11.2026 mit bis zu 20 Stunden pro Woche. 400 Rechnungen abgestimmt."
        notes = [f["note"] for f in check.scan(output, genre="cv", lang="de", source=source)["findings"] if f["id"] == "F2"]
        self.assertTrue(any("added" in n for n in notes))
        self.assertTrue(any("dropped" in n for n in notes))

    def test_code_tokens_match_by_part(self):
        result = check.scan("Englisch auf C1-Niveau.", lang="de", source="Englisch C1")
        self.assertNotIn("F1", ids(result))

    def test_need_markers_listed(self):
        result = check.scan("Dear team, [NEED: which paper] caught my eye.", lang="en", source="notes")
        self.assertEqual(len(result["needs"]), 1)
        self.assertFalse(any(f["id"] == "F3" for f in result["findings"]))


class CounterTests(unittest.TestCase):
    def test_cloned_bullets(self):
        text = ("- Spearheaded A, leveraging X, resulting in 5% gains\n"
                "- Orchestrated B, leveraging Y, resulting in 6% gains\n"
                "- Championed C, leveraging Z, resulting in 7% gains\n")
        self.assertIn("R7", ids(check.scan(text, genre="cv", lang="en")))

    def test_mixed_address_forms(self):
        text = "Sehr geehrte Frau Keller, gern sende ich Ihnen die Unterlagen. Du kannst mich jederzeit anrufen."
        self.assertIn("G4", ids(check.scan(text, genre="prose", column="letter", lang="de")))

    def test_language_detection(self):
        self.assertEqual(check.detect_language("Das ist nicht der Punkt, und wir wissen das."), "de")
        self.assertEqual(check.detect_language("This is not the point, and we know it."), "en")


if __name__ == "__main__":
    unittest.main()
