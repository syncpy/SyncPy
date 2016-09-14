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

# Download SyncPy
echo "Getting SyncPy..."
curl -sSL https://github.com/syncpy/SyncPy/archive/master.zip -o master.zip

unzip -qq master.zip

# Install SyncPy in /
sudo cp -R SyncPy-master/v1.2 /SyncPy/

sudo chmod -R 777 /SyncPy/

rm -R SyncPy-master
rm master.zip

# Create a shortcut to the interface on the user's desktop
if [ -f $HOME/Desktop/SyncPy ]; then
    rm $HOME/Desktop/SyncPy
fi
touch $HOME/Desktop/SyncPy

echo "#!/bin/bash" >> $HOME/Desktop/SyncPy
echo "cd /SyncPy/interface/sources/" >> $HOME/Desktop/SyncPy
echo "python MainWindow.py" >> $HOME/Desktop/SyncPy

sudo chmod +x $HOME/Desktop/SyncPy

echo "SyncPy installed in /SyncPy/ - Interface shortcut created on the Desktop"
