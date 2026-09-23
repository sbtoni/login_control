# Login Control 

Custom Home Assistant component for clearing all tokens of specific user 

Usage:
1. Add `login_control:` to the configuration yaml of your HA instance
2. Get the User ID of the user that you want to clear (In HA, go to Configuration -> Persons -> Users -> Press on your user name. Window will open that will show your ID.)
3. Call `clear_refresh_tokens` service with `user_id` parameter with User ID that you retrieved in step 1.

Changes:
  - mode: inactive (only inactive tokens)  all (all tokens including active ones)
  - days: 5 (If mode: inactive , removes token if last refresh is older that days:)
  - all_users: true (if true, checks for all users, no need to specify an user_id. If false user_id: needs to be set)
  - user_id: <userID> User ID as described in the info. Not changed.

Usage:
  - action: login_control.clear_refresh_tokens
    metadata: {}
    data:
      mode: inactive
      days: 7
      all_users: true

  - action: login_control.clear_refresh_tokens
    metadata: {}
    data:
      mode: all
      all_users: false
      user_id:  <userID from HA>
