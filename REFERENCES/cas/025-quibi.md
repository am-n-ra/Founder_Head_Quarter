---
case: Quibi
founder: Jeffrey Katzenberg (CEO), Meg Whitman (Chair)
problem: "People waiting in lines or during commutes want premium short-form video (10-min episodes)"
sacrifice: "Katzenberg left DreamWorks Animation (sold to Comcast), invested $1B+ of raised capital"
sacrifice_type: career_and_reputation
demo: "Platform built before launch — 7,000 episodes commissioned, no MVP testing"
distribution_type: open
incorporation: day-one
inflection: "COVID lockdown (2020) destroyed the use case (commuting) 2 weeks after launch"
inflection_type: negative
growth_stages:
  G1_pmf:
    method: "No PMF measurement — launched with 7,000 commissioned episodes before testing whether users wanted the format"
    pmf_signal: "None — no Sean Ellis test, no retention measurement before full launch"
    result: "10M downloads but only 1.3M active users after 90-day free trials expired. Retention collapsed to near-zero after the trial window."
    verdict: "PMF never existed. The 40% threshold, if measured, would likely have been below 10%."
  G2_repeatable:
    result: "Never reached G2. Shut down 6 months after launch."
    note: "Attempted to skip G1 entirely — spent $1.75B on content and infrastructure before validating demand."
invariants:
  problem_precedes: false
  sacrifice_real: true
  positioning_before_believer: false
  inflection_unpredictable: true
phase_dates:
  genese: "2017"
  sacrifice: "2018"
  demo: "none — no MVP"
  distribution: "2020-04"
  early_believer: "2018-2020"
  incorporation: "2018"
  inflexion: "2020-04"
---
# Quibi — Premature Scaling Case Study

## Why This Case Matters

Quibi is the most expensive premature scaling case in modern startup history: **$1.75B raised, shut down 6 months after launch, $1.1B returned to investors.** It's the Startup Genome finding (70-74% of failures from premature scaling) rendered in real numbers with clean, public data.

## G1 — Never Searched

Quibi spent $1.75B without ever answering the question "do users actually want this?"

- **$1.1B on content**: 7,000 episodes commissioned before launch. Multiple shows with A-list talent (Steven Spielberg, Jennifer Lopez, Chance the Rapper).
- **$175M on marketing**: Launch campaign across Super Bowl, digital, outdoor.
- **$0 on PMF validation**: No MVP. No pilot. No Sean Ellis test. No soft launch.
- **Zero retention engineering**: The product required users to *pay* after a 90-day trial. When trials expired, active users dropped from ~10M downloads to ~1.3M.
- **Wrong segment**: The entire thesis (short-form video for commuters) was destroyed by COVID — but even in a normal world, "premium content for waiting" had no demonstrated demand.

**The Sean Ellis test, if run**: The best-case estimate for "very disappointed" among Quibi's users after the trial would have been well under 10%. The product solved a problem users didn't feel (they were fine with TikTok, YouTube, Netflix, or just waiting).

## Premature Scaling: What Actually Happened

Quibi followed the exact pattern Startup Genome identified as the #1 killer:

| Premature Scaling Signal | Quibi's Reality |
|--------------------------|-----------------|
| Spend on growth/scale before PMF proven | $1.75B raised and spent before any demand validation |
| Hire execs before proving product works | 200+ employees, senior Hollywood + Silicon Valley execs, $100M+ annual burn pre-launch |
| Commission supply before demand exists | 7,000 episodes, 50+ shows, before knowing if anyone wanted 10-min formats |
| Skip MVP / soft launch | Full global launch on day one with no pilot market |

**The counterfactual**: If Quibi had spent $5M on a 3-month MVP test (10 episodes, one city, 1,000 users), they would have discovered the retention collapse before spending $1.7B. The PMF test costs $0 if you run it before building. Quibi ran it after spending everything.

## Inflection (Negative)

COVID was an unpredictable inflection, but it accelerated a death that was already inevitable. Quibi's retention data after the 90-day trial showed <10% conversion — COVID didn't cause the failure, it just made the investors admit it faster. The thesis (premium short-form for commuters) was untested and, when tested, unsupported.

## What This Case Verifies

1. **Premature scaling is the #1 killer**: Quibi is a $1.75B proof of the Startup Genome 70-74% finding. The spend preceded the validation, and the validation never came.
2. **PMF measurement is not optional**: $1.75B was lost because nobody ran a $0 survey (Sean Ellis test) before spending on content.
3. **Inflection unpredictability (negative)**: COVID destroyed the commuting thesis — but a venture that had tested PMF would have discovered the thesis was weak even without COVID.
4. **Skipping G1 guarantees G2 never arrives**: Quibi went from incorporation straight to "spend like PMF exists" — and collapsed.
5. **The sacrifice invariant was met (Katzenberg burned his reputation and career capital) but the problem-precedes-company invariant was violated**. The invariants held: violating any one leads to failure.

## Sources

- WSJ: "Quibi's $1.75B Lesson" (2020)
- The Information: "Quibi's Rise and Fall" (2020)
- TechCrunch: "Quibi Shuts Down" (Oct 2020)
- Startup Genome Report (2019, 2020) — premature scaling findings
- Variety & Hollywood Reporter: Quibi content spend analysis
- SEC filings: Quibi fundraising and dissolution
