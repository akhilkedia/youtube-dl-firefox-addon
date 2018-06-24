/*
On startup, connect to the 'ping_pong' app.
*/
console.log('Starting firefox command runner!')
var port = browser.runtime.connectNative('firefox_command_runner');

/*
Log that we received the message.
Then display a notification. The notification contains the URL,
which we read from the message.
*/
function notify(message) {
  console.log('background script received message');
  browser.notifications.create({
    'type': 'basic',
    'iconUrl': browser.extension.getURL('icons/message.svg'),
    'title': 'Received Message from Backend!',
    'message': message,
  });
}

/*
Assign `notify()` as a listener to messages from the content script.
*/
port.onMessage.addListener(notify);

/*
On a click on the browser action, send the app a message.
*/
browser.browserAction.onClicked.addListener(function(tab) {
  console.log('Sending: ' + tab.url);
  port.postMessage(tab.url);
});
