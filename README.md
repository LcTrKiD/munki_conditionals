# munki_conditionals
A collection of conditional items scripts for munki.

### kext_mdm_conditions
- Generates two conditions, `kext_bundles` and `kext_teams` which contain an array of the Bundle ID and Team ID of any KEXT Whitelist/Blacklist that is deployed via MDM.

### pppcp_conditions
- Generates a simple list of any PPPCP identifiers (`bundleID` or `path`) that have been deployed via MDM to a client. This can be used to do a simple determination of an expected PPPCP profile has been deployed to a client device.
- - Can then use a predict like `ANY pppcp_payloads == 'com.apple.Terminal'` to make a package available to `munki` to deploy to a client.
