# Salesforce-Trailhead-Api-Hack

This is a hack implementation to get access to Trailhead API to get Trailhead user points and other attributes.
Requests should be used in the form
https://trailheadapi.herokuapp.com/?link=/id/userAlias

It is possible to deploy code to your own heroku instance


## Possible error
Sometimes Salesforce changes the way it retrieves data internally for Trailhead data. In such cases `aura:clientOutOfSync` error happens. https://salesforce.stackexchange.com/questions/132694/auraclientoutofsync-exception-when-calling-from-lightning-after-a-while
In such case update to code is needed to conform with newest changes.
