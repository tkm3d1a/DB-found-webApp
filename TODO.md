## Tasks

### SQL Tasks

- [x] TODO: Create analysis table
  - [x] Main Table creation
    - does not includie updating all custom calculations yet
  - [x] Park-adjusted runs created
    - Calculation is done by pulling info from the Teams Table, BPF
      1. Create RC table
      2. Use home field as BPF value for a player
      3. Adjustment percent = BPF + 100 / 200
      4. PARC = RC/Adjustment percent
  - [x] Park-adjusted runs created per 27 outs
    - same calculation as above, just using RC27 instead of RC
  - [ ] Any other benefical items to add?
- [x] TODO: Create a summary table?
  - This could be a way to link player full names a little better?
  - Or an easier link from someone inserting a name to get to a playerid
  - [TK] Summary table seemes not needed.  Can use different query and joins to get needed values no problem
- [x] TODO: Create trigger to update tables as needed?
  - Triggers not really needed, so can close this out

### Python/Website tasks

- [x] TODO: Setup user auth as module for flask env
  - User Log in works
  - Can register
  - does not allow duplicate username or emails
  - Passwords stored as hash (no Plain text password storage)
- [ ] TODO: ORM for neede info to be dev
  - [x] ORM for Analysis created
  - [x] ORM for People table for name look ups
  - [x] ORM for webusers
  - [ ] ORM for saved searches
- [x] TODO: Search field for searching by first and last name
  - First and last name are currently seperated
  - If one result, returns that result directly
  - If multiple results, returns the list, and then a drop down for user to select what player they wanted
    - [x] TODO: Feature not fully working, errors when submitting selection
      - Possible causes:
        - hitting submit submits the form with no values
        - this hits the check that the search fields have values to avoid returning entire DB when searching
        - [x] TODO: Implment this feature fully
        - Search now works from both multiple results page and if a single result is found
- [ ] TODO: Way to save a users preferences/favorite players
- [x] TODO: Format output of table
  - Its formatted as a simple table, not pretty
  - Need to see if any other columns need to be added
    - Columns currently match the reference image

### Misc Tasks

- [ ] TODO: Add TOC here for readme
- [ ] TODO: Make sure to update [Worklog](#worklog) with each PR or commit
  - Format for update should be:
    - Date in italics
    - Initials of commenter in square brackets
    - Bullets with each main change
- [ ] TODO: Add link for MariaDB install
- [ ] TODO: Add instructions for setting up base DB instance
- [ ] TODO: User info setup required as well
- [ ] TODO: decomp requirements for assigning tasks 
  - Tim and Kevin todo
  - (complete by 11-5-22)
- [ ] TODO: gather reference material and images
- [ ] TODO: Mark todo lines with assignee names if possible to avoid double work
- [ ] TODO: Work on installation instructions for setting up DB
  - Tim to do (no date set)