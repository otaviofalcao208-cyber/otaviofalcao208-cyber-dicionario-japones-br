const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const sw = fs.readFileSync('sw.js', 'utf8');
new vm.Script(sw, {filename:'sw.js'});
const events = {};
const self = {addEventListener(name, callback) {events[name]=callback;}, skipWaiting:async()=>{},clients:{claim:async()=>{}}};
const cacheData = new Map();
const cache = {
 async put(key,response){cacheData.set(String(key.url||key),response.clone());},
 async match(key){return cacheData.get(String(key.url||key))?.clone();}
};
let networkCalls=0;
class ResponseMock {
 constructor(body, options={}){this.body=body;this.ok=true;this.status=options.status||200;this.type='basic';this.headers=options.headers||{};}
 clone(){return new ResponseMock(this.body,{status:this.status,headers:this.headers});}
 async text(){return this.body;}
 static error(){return {ok:false,status:0};}
}
const context={self,URL,Response:ResponseMock,Request:class{constructor(url){this.url=String(url.url||url);this.method='GET';this.mode='same-origin';}},caches:{open:async()=>cache,keys:async()=>[],delete:async()=>{}},fetch:async()=>{networkCalls++;return new ResponseMock('online');},console};
vm.createContext(context);
vm.runInContext(sw,context);
assert.equal(typeof events.install,'function');
assert.equal(typeof events.activate,'function');
assert.equal(typeof events.fetch,'function');
const addScripts=vm.runInContext('addWordScripts',context);
const once=addScripts('<html><body></body></html>');
for(const v of [196,197,198,199]) assert.equal(once.split('palavras-v'+v+'.js').length-1,1);
assert.equal(addScripts(once),once,'não duplicar scripts');
assert.equal(addScripts('<body><script src="./palavras-v199.js?v=199"></script></body>').split('palavras-v199.js').length-1,1);
(async()=>{
 const request={url:'https://example.com/app/tracos.js',method:'GET',mode:'same-origin'};
 await cache.put(request,new ResponseMock('cached'));
 let response;
 events.fetch({request,respondWith(p){response=p;},waitUntil(){}});
 assert.equal(await (await response).text(),'cached');
 assert.equal(networkCalls,0,'cache estático não deve aguardar a rede');
 for(const asset of ['tracos.js','kanji-dados.js','index.html','pratica.html']) assert(sw.includes('"./'+asset+'"'));
 console.log('OK: sintaxe, scripts sem duplicação, cache prioritário e recursos offline.');
})().catch(e=>{console.error(e);process.exitCode=1;});
