# This file is used to check for updated to the addon

import urllib.request

# currentVersion is a string formatted like "1.2.3". No leading zeros
def isUpdateAvailable(currentVersionTuple):
    print("checking for updates...")
    result = False   # Default to no update
    with urllib.request.urlopen('https://raw.githubusercontent.com/jdavies/settings_mgr/master/settings_mgr/version.txt') as response:
        html = response.read()
        latestVersionTuple = html.decode('UTF-8').split('.')
        # Convert to an integer
        latestVersion = int(latestVersionTuple[0]) * 100 + int(latestVersionTuple[1]) * 10 + int(latestVersionTuple[2])
        currentVersion = int(currentVersionTuple[0]) * 100 + int(currentVersionTuple[1]) * 10 + int(currentVersionTuple[2])
        print("comparing " + str(latestVersion) + " = " + str(latestVersion) + " to " + str(currentVersion) + " - " + str(currentVersionTuple))
        result = latestVersion > currentVersion
        print("   Result: " + str(result))
    return result

if __name__ == "__main__":
    # Code works when testing against the results "1.0.2"
    # This will nott work when testing aagainst the live 
    # version number on Github
    print(isUpdateAvailable((0, 0, 2)))
    assert isUpdateAvailable((0, 0, 2)) == False
    # print(isUpdateAvailable((0, 0, 3)))
    # print(isUpdateAvailable((1, 0, 0)))
    # print(isUpdateAvailable((0, 1, 1)))
    # print(isUpdateAvailable((2, 0, 0)))
    # assert isUpdateAvailable((2, 0, 0)) == False
    # print(isUpdateAvailable((1, 1, 0)))
    # print(isUpdateAvailable((1, 0, 3)))
    # print(isUpdateAvailable((1, 0, 2)))