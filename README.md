# Wilford

Do you like listening to LDS General Conference talks? Do you wish you had a girlfriend? Do you need a way to download General Conference talks in bulk?

**Wilford** can help you with 2 of those!

**Wilford** is a simple text-based program that lets you download General Conference Talks from the [Church of Jesus Christ of Latter-day Saints](https://churchofjesuschrist.org/study/general-conference) by speaker.

**WARNING**
This program is kind of janky when compiled. You might just have a better experience downloading the source code than trying to run it from the "executable" in the release

## Install Wilford

If you want to try out **Wilford**, then you have two options:
_Remember this is a beta program built by a random college kid. There are a million problems with this. I'm keeping track of things to do [here](https://github.com/users/DallinFromEarth/projects/4)_


[Click here](https://github.com/DallinFromEarth/Wilford/releases/latest) to download the latest release of Wilford. Download the file based on your operating system. (`wilford-macos` for Mac, etc)

### macOS
1. Download both `wilford-macos-vX.X.X` and `install-mac.sh`
2. Open Terminal in the download directory
3. Run these commands to get macOS to let you run the code:
   ```bash
   chmod +x wilford-macos       
   xattr -rd com.apple.quarantine wilford-macos
   ```
4. When running for the first time, you'll need to:
   - Right-click the executable
   - Select 'Open'
   - Click 'Open' in the security dialog

### Windows
Simply download and double-click `wilford-windows.exe`. Windows may show a security warning since the app isn't signed - click "More info" and then "Run anyway" to proceed.

### Linux
_I don't use Linux, so these install steps come from our AI friend Claude. Trust at your own peril._
1. Download `wilford-linux`
2. Open Terminal in the download directory
3. Make it executable:
   ```bash
   chmod +x wilford-linux
   ```
4. Run it:
   ```bash
   ./wilford-linux
   ```

Alternatively, move it to a directory in your PATH:
```bash
sudo mv wilford-linux /usr/local/bin/wilford
wilford
```