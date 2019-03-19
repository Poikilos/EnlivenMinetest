# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [git] - 2019-03-19
### Added
- skin uploading via webapp (chooses Bucket_Game, or ENLIVEN if present)
- `npm install formidable mv` (switched from fs.rename to mv due to
  rename not working across filesystems (tmp is commonly on a different
  volume).
