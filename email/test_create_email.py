# pylint:skip-file

import pytest

from create_email import write_email


def test_write_email():
    hearing = [
        {'hearing_citation': '[2025] UKFTT 1192 (GRC)',
         'hearing_title': 'Devtech Security Limited v The Pensions Regulator',
         'hearing_description': 'This hearing concerns an appeal by a company against a £400 fixed penalty notice issued for failing to submit a Declaration of Compliance within the prescribed deadline. The company argued that only an eligible employee (their mother) was involved in auto-enrolment, that they acted in good faith, and that the penalty was unfair. The Respondent sought to strike out the reference, claiming lack of jurisdiction, citing case law. The court considered jurisdictional issues, evidence regarding the timing of awareness and actions taken, and the circumstances leading to the missed deadline. The key dispute was whether the Tribunal had jurisdiction to hear the case and the validity of the penalty.',
         'hearing_anomaly': 'None Found',
         'hearing_url': 'https://caselaw.nationalarchives.gov.uk/ukftt/grc/2025/1192',
         'judgement_favour': 'Plaintiff'}
    ]

    assert len(write_email(hearing)) > 0
