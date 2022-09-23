backup_directory=../backups/project
rm -rf $backup_directory
rsync -r .. $backup_directory
cd $backup_directory || exit
rm -rf .git
git init
git add .
git clean -fdx
rm -rf .git
