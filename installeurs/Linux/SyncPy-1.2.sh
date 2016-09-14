#!/bin/bash

# Download and install Anaconda if not installed
if ! [ -d "$HOME/anaconda" ]; then
    echo "Getting Anaconda..."
    wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-Linux-x86_64.sh --no-check-certificate

    bash Anaconda-2.3.0-Linux-x86_64.sh -b -p $HOME/anaconda

    cp $HOME/.profile $HOME/.profile.syncpysave

    echo -e "\n#ADDED BY SYNCPY\nPATH=$HOME/anaconda/bin:$PATH" >> $HOME/.profile

    . $HOME/.profile

    rm Anaconda-2.3.0-Linux-x86_64.sh

else

    echo "Anaconda is already installed"

fi

# Download SyncPy
echo "Getting SyncPy..."
wget https://github.com/syncpy/SyncPy/archive/master.zip --no-check-certificate

unzip -qq master.zip

# Install SyncPy in /
sudo cp -R SyncPy-master/v1.2 /SyncPy/

sudo chmod -R 777 /SyncPy/

rm -R SyncPy-master
rm master.zip

# Create a shortcut to the interface in /home/user
if [ -f $HOME/SyncPy ]; then
    rm $HOME/SyncPy
fi
touch $HOME/SyncPy
cd ..
echo "#!/bin/bash" >> $HOME/SyncPy
echo "cd /SyncPy/interface/sources/" >> $HOME/SyncPy
echo "python MainWindow.py" >> $HOME/SyncPy

sudo chmod +x $HOME/SyncPy

echo "SyncPy installed in /SyncPy/ - Interface shortcut created in the home folder"
