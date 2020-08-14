#!/bin/bash
echo 'Building React Application'
npm run build
echo 'Cleaning templates and static folders'
find ../templates/ -mindepth 1 -maxdepth 1  -not -name .gitkeep -exec rm -rv {} \;
find ../static/ -mindepth 1 -maxdepth 1  -not -name .gitkeep -exec rm -rv {} \;
echo 'Moving build files'
mv build/static/* ../static/
rm -r build/static
mv build/* ../templates