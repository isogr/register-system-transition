Given a path to GR directory
(a directory with register.yaml, see https://github.com/isogr/registry/tree/master/gr-registry)
and a path to an extent map file, outputs proposal (in importable JSON format)
to add relevant extents as separate items and clarify items that use extents
to refer to relevant extent item IDs.

Proposal details pertaining to data model:

- Extent class ID: ``extent``
- Top-level attribute name for extent data on items that have it: ``extent``
- Top-level attribute name to use for extent reference: ``extentRef``
- The pre-existing extent data is not changed or removed, only ``extentRef``
  is added

Extent map file is a text file where each line corresponds to a distinct extent and contains,
separated by white space or tab:

- Items that use this extent, as a list of comma-separated (with possible whitespace)
  item IDs enclosed in square brackets.
  The first item is used for extent data (description, bounds)
- Extent bounds, as four decimal numbers. Used for cross-reference
- Extent *name* to use.

Example extent map file line::

    [773, 469]	-110	60	-120	49	Canada - Alberta			

Requirements: Node 20, Yarn 4.2.

Usage::

    yarn generate-extent-migration-proposal --registry-dir /path/to/gr/registry --out-json test.json --extent-map /path/to/extents.txt --stakeholder-username <git-username> --register-version <version>
