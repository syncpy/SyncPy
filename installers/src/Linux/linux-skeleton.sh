#!/bin/bash

# Download and install Anaconda if not installed
if ! [ -d "$HOME/anaconda" ]; then
    echo "Getting Anaconda..."
    wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-Linux-x86_64.sh --no-check-certificate

    bash Anaconda-2.3.0-Linux-x86_64.sh -b -p $HOME/anaconda

    cp $HOME/.profile $HOME/.profile.syncpysave

    echo -e "\n#ADDED BY SYNCPY2\nPATH=$HOME/anaconda/bin:$PATH" >> $HOME/.profile

    . $HOME/.profile

    rm Anaconda-2.3.0-Linux-x86_64.sh

else

    echo "Anaconda is already installed"

fi

# Download SyncPy2
echo "Getting SyncPy2..."
wget https://github.com/syncpy/SyncPy/archive/master.zip --no-check-certificate

unzip -qq master.zip

# Install SyncPy2 in /
sudo cp -R SyncPy-master/vX.X /SyncPy2/

sudo chmod -R 777 /SyncPy2/

rm -R SyncPy-master
rm master.zip

# Create a shortcut to the interface in /home/user
if [ -f $HOME/SyncPy2 ]; then
    rm $HOME/SyncPy2
fi
touch $HOME/SyncPy2
cd ..
echo "#!/bin/bash" >> $HOME/SyncPy2
echo "cd /SyncPy2/src/" >> $HOME/SyncPy2
echo "python SyncPy2.py" >> $HOME/SyncPy2

sudo chmod +x $HOME/SyncPy2

# Create a shortcut to the module wizard in /home/user
if [ -f $HOME/SyncPy2MethodWizard ]; then
    rm $HOME/SyncPy2MethodWizard
fi
touch $HOME/SyncPy2MethodWizard
cd ..
echo "#!/bin/bash" >> $HOME/SyncPy2MethodWizard
echo "cd /SyncPy2/src/" >> $HOME/SyncPy2MethodWizard
echo "python SyncPy2MethodWizard.py" >> $HOME/SyncPy2MethodWizard

sudo chmod +x $HOME/SyncPy2MethodWizard

echo "SyncPy2 installed in /SyncPy2/ - Shortcuts created in the home folder"
