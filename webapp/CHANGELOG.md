# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [git] - 2019-03-19
### Added
- skin uploading via webapp (chooses Bucket_Game, or ENLIVEN if present)
- choosing existing (non-player `skin_*.png`) files
- `npm install multer`
  - mv is no longer needed--had switched from fs.rename to mv due to
  rename not working across filesystems (tmp is commonly on a different
  volume), but then switched from formidable to multer since multer has
  built-in functionality to cancel upload if too large, but formidable
  crashes (see <https://stackoverflow.com/a/27067596/4541104>), so mv is
  no longer needed)
