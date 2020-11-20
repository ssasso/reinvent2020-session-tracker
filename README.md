# reinvent2020-session-tracker
Decent Session Tracker for re:Invent 2020

re:Invent 2020 session list is a bit confusing.
It's impossible to see a "merged" view (i.e. Session Title with different availability slots), insead of a full "repeated" list.

Looking at the HTML page, all the sessions are stored in JSON format approx here:
```
$(document).ready(function() {
    kmsReact.ReactDOM.render(kmsReact.React.createElement(kmsReact.Pages.EventPlatform.Agenda,
        {"tab":"","filters":[{"label":"Tracks","allValuesElement":"All Tracks",
```
so it should be possible to take this JSON structure and parse it in a more decent way.
