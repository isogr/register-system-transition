NOTE: WIP, not yet operational.

Given a path to GR directory
(a directory with register.yaml, see https://github.com/isogr/registry/tree/master/gr-registry)
and a path to an citation map file, outputs proposal (in importable JSON format)
to add relevant citations as separate items and clarify items that use citations
to refer to relevant information source item IDs.

Proposal details pertaining to data model:

- Information source class ID:
  ``information-source``
- Top-level attribute name for the list of citations:
  ``informationSources``
- Top-level attribute name to use for the list of information source references:
  ``informationSourceRefs``
- The pre-existing citations are not changed or removed,
  only ``informationSourceRefs`` is added

Citation map file is a CSV file where each line corresponds
to a distinct information source and contains:

- Citation occurrences of this information source,
  as a list of unique space-separated ``<itemID>-<citationNumber>`` items,
  where item ID is GR item ID (positive integer) and citation number
  is 0-based index of citation in the list (since one item can have multiple
  citations).

- Information source register item data, each in its own column:

  - title
  - author
  - publisher
  - edition
  - editionDate
  - revisionDate
  - seriesName
  - seriesIssueID
  - seriesPage
  - isbn
  - issn
  - otherDetails

Example citation map file line::

    473-0 606-0 210-1 228-1 414-1 114-0,A Refinement to the World Geodetic System 1984 Reference Frame,"M. J. Merrigan, E.R. Swift, R.F. Wong, Saffel J.T.",Institute of Navigation,,,,"Proceedings of the 15th International Technical Meeting of the Satellite Division of The Institue of Navigation (ION-GPS-2002), Portland, OR, September 2002",,1519-1529,,,

Requirements: Node 20, Yarn 4.2.

Usage::

    yarn generate-citation-migration-proposal --registry-dir /path/to/gr/registry --out-json test.json --citation-map /path/to/citations.csv --stakeholder-username <git-username> --register-version <version>

Register version is the UUID of latest accepted proposal.
