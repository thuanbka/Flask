const CACHE_NAME = 'my-cache';

self.addEventListener('install', event => {
  console.log("Service worker installed!!");
});

self.addEventListener('fetch', event => {
    console.log("Get request to "+ event.request.url);
});
