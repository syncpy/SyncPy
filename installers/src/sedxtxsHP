#!/bin/bash

# Download and install Anaconda if not installed
if ! [ -d "$HOME/anaconda" ]; then
    echo "Getting Anaconda..."
    curl -sSL https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-MacOSX-x86_64.pkg -o Anaconda-2.3.0-MacOSX-x86_64.pkg

    sudo installer -pkg Anaconda-2.3.0-MacOSX-x86_64.pkg -target /

    sudo mv /anaconda/ $HOME

    sudo cp $HOME/.profile $HOME/.profile.syncpysave

    cat $HOME/.profile | sed -e "s#//anaconda#$HOME/anaconda#g" > $HOME/.profiletmp

    mv $HOME/.profiletmp $HOME/.profile

    . $HOME/.profile

    rm Anaconda-2.3.0-MacOSX-x86_64.pkg

else

    echo "Anaconda is already installed"

fi

# Download SyncPy2
echo "Getting SyncPy2..."
curl -sSL https://github.com/syncpy/SyncPy/archive/master.zip -o master.zip

unzip -qq master.zip

# Install SyncPy2 in /
sudo cp -R SyncPy-master/v2 /SyncPy/

sudo chmod -R 777 /SyncPy2/

rm -R SyncPy-master
rm master.zip

# Create a shortcut to the interface on the user's desktop
if [ -f $HOME/Desktop/SyncPy2 ]; then
    rm $HOME/Desktop/SyncPy2
fi
touch $HOME/Desktop/SyncPy2

echo "#!/bin/bash" >> $HOME/Desktop/SyncPy2
echo "cd /SyncPy2/src/" >> $HOME/Desktop/SyncPy2
echo "python SyncPy2.py" >> $HOME/Desktop/SyncPy2

sudo chmod +x $HOME/Desktop/SyncPy2

# Create a shortcut to the module wizard on the user's desktop
if [ -f $HOME/Desktop/SyncPy2MethodWizard ]; then
    rm $HOME/Desktop/SyncPy2MethodWizard
fi
touch $HOME/Desktop/SyncPy2MethodWizard

echo "#!/bin/bash" >> $HOME/Desktop/SyncPy2MethodWizard
echo "cd /SyncPy2/src/" >> $HOME/Desktop/SyncPy2MethodWizard
echo "python SyncPy2MethodWizard.py" >> $HOME/Desktop/SyncPy2MethodWizard

sudo chmod +x $HOME/Desktop/SyncPy2MethodWizard

echo "SyncPy2 installed in /SyncPy2/ - Shortcuts created on the Desktop"
