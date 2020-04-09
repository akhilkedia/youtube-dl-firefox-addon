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

/* thanks @Lemmon Hill for https://github.com/lennonhill/cookies-txt */
function formatCookie(co) {
  return [
    [
      co.httpOnly ? '#HttpOnly_' : '',
      !co.hostOnly && co.domain && !co.domain.startsWith('.') ? '.' : '',
      co.domain
    ].join(''),
    co.hostOnly ? 'FALSE' : 'TRUE',
    co.path,
    co.secure ? 'TRUE' : 'FALSE',
    co.session || !co.expirationDate ? 0 : co.expirationDate,
    co.name,
    co.value + '\n'
  ].join('\t');
}

/*
Assign `notify()` as a listener to messages from the content script.
*/
port.onMessage.addListener(notify);


/*
On a click on the browser action, send the app a message.
*/
browser.browserAction.onClicked.addListener(function(tab) {
  console.log('getting cookies for ' + tab.url);
  browser.cookies.getAll({url: tab.url}, function(cookie_list) {
    console.log('found ' + cookie_list.length + ' cookies');
    console.log('Sending: ' + tab.url);
    port.postMessage(JSON.stringify({url: tab.url, cookies: cookie_list.map(formatCookie)}));
  });
});
