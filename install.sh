#! /usr/bin/bash 

NEW_DIR_NAME="Custom Scripts"

cd $HOME 
mkdir "$NEW_DIR_NAME"
cd "$NEW_DIR_NAME"

NEW_DIR_PATH="$HOME/$NEW_DIR_NAME"
git clone https://github.com/ShaderOX/CGet.git
cd CGet
cp cget.py utils.py ../
python3 install -r requirements.txt
cd ..
rm -rf ./CGet/
echo "alias cget=\"python3 '$NEW_DIR_PATH/cget.py'\"" >> "$HOME/.bashrc" 
echo Done!
