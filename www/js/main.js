var socket;

var connected = 0;
var cnt = 0;

var dic = [];

function start(){
	document.querySelector('core-list').data = [{"index": 0}, {"index": 1}, {"index": 2}];

}
function init(){
  //alert("init");

}

function startingStartPage(){
	$( '.initpage' ).hide();
	$( '.startpage' ).show();
	getMacAddress();
}

function startSearchBT(){
	$( '.startpage' ).hide();
	$( '.mainpage' ).show();
	scanBT();
}

function showInfomation( target ){
	
	sendData( JSON.stringify(
	{
		'type':'query',
		'mac':target
	}
		) );
	$( '.cardpage' ).show();
	$( '.mainpage' ).hide(); 
}



function handleEvent( response ){

	//alert( JSON.stringify( response ) );

	if ( response['type'] == 'conn_response' ){
		if ( response['success'] == 'true' )
			connected = true;
	}
	else if ( connected ){
		
	

		if ( response['type'] == 'matchtag_response' )	{


					

			if ( response['success'] == 'true' ){

				try{


				var showList = document.getElementById( "btlist" );

				var tags = ' ';
				var tag_pool = response['tags'];

				for ( var i = 0 ; i < tag_pool.length ; i++ ){
					tags += '#'+tag_pool[i];
					tags += "  ";
				}

				
 				var newdiv = '<div class="item item-row" id="'+response['name'];
 					newdiv += '">';
                    newdiv +=  '      <img src="img/pic1.png" class="item-img"> ';
                    if ( cnt > 0 )
                    newdiv +=  '      <img src="img/keyboard53-3.png" class="item-img-footer"> ';
                    newdiv +=  '      <span class="item-inside"> ';
                    newdiv +=  '            <div>			     ';
                    newdiv +=  '     <div class="item-name"> <span class="hh1"> '
                    
                    if ( cnt > 0 )
                   	 	newdiv +=  response['name'];
                   	else 
                   		newdiv +=  response['name'] + " - ME";
                    newdiv +=  '</span> </div>';
                    newdiv +=  '     <div class="item-name"> <span class="hh3 tag">';
                    newdiv += tags;
                    newdiv +=  '</span></div> ';            
                    newdiv +=  '     </div> </span> </div>';                                         
         			
                   

        			dic.push(response['name']);
         			cnt += 1;
        			$( '#btlist' ).append( newdiv );

         	       	//showList.innerHTML += newdiv;

         	       	var t = '#'+response['name'];
         	       	var item = response['target'];

         	       	$( t ).click( function(){ showInfomation( item ) } );
         	       	
         	       	/*
	         	      for (var t in dic){

	                    index="#"+dic[t];

	                    $(index).click(function() {

	                        showInfomation( dic[t] );
	                    });
	                  }
	                  */
				}
				catch( err ){
					alert( err.message );

				}
			}
		}
			else if ( response['type'] == 'query_response'  ){

				

				try{
				if ( response['success'] == 'true' ){

					var socialData = response[ 'query' ];
					var tags       = response[ 'tags' ];
					var name = socialData[1];
					var fb = socialData[3];
					var twitter = socialData[6];
					var ig = socialData[5];
					var imgLink = socialData[7];
		
					document.getElementById( "user_name" ).innerHTML = name;
					
					$( '#avatar' ).attr( 'src' , imgLink );


					for ( var i = 0 ; i < tags.length ; i++ ){
						document.getElementById("tag"+(i+1)).innerHTML = '<i class="tag icon"></i>' + tags[i];
					}

					document.getElementById("btn1").onclick = 
					function(){ 
						
						navigator.notification.alert(fb, function(){}, "FB", "ok"); 
					};
					document.getElementById( 'btn2' ).onclick = 
					function(){ 
						navigator.notification.alert(twitter, function(){}, "TWITTER", "ok"); 
					};
					document.getElementById( 'btn3' ).onclick = 
					function(){ 
						navigator.notification.alert(ig, function(){}, "INSTAGRAM", "ok"); 
					};

				}
				}
				catch( err ){
					alert( err.message );
				}

			}



				






	}


}

function logIn( macAddress ){

	socket = new Socket();
	socket.onData = function(data) {
		var str = String.fromCharCode.apply(null, data);
		var obj = str.split( '\n' );

		for ( var i = 0 ; i < obj.length-1 ; i++ )
			handleEvent( JSON.parse( obj[i] ) );

	};
	socket.onError = function(errorMessage) {
	  // invoked after error occurs during connection
	  //alert('dog');
	};
	socket.onClose = function(hasError) {
	  // invoked after connection close
	  alert('connection closed');
	  connected = false;
	};
	socket.open(
	  "140.113.27.54",
	  8888,
	  function() {
	    // invoked after successful opening of socket
	    sendData(JSON.stringify( {'type':'conn','mac':macAddress}  ));
	    onDiscoverDevice( {'id':macAddress} );
	  },
	  function(errorMessage) {
	  	alert( errorMessage.message );
	    // invoked after unsuccessful opening of socket
	  });

}

function sendData(dataString){	
	    	//alert( dataString + " " + dataString.length);
	    dataString += '\n';
		var data = new Uint8Array(dataString.length);
		for (var i = 0; i < data.length; i++) {
		data[i] = dataString.charCodeAt(i);
		}
		socket.write( data );
}

function onDiscoverDevice( device ){
	
	sendData( JSON.stringify( { 'type':'matchtag' , 'target':device['id'] } ) );
}

function onDiscoverDevice2( devices ){
 	devices.forEach(function(device) {
        sendData( JSON.stringify( { 'type':'matchtag' , 'target':device.address } ) );
    });

}

function onNoneDiscoverDevice2( device ){


}


function onNoneDiscoverDevice( device ){


}

function getMacAddress(){
	var ret = 'mac Address get failure';

	window.MacAddress.getMacAddress(
		function(macAddress) {  
			logIn( macAddress );
		},
		function(fail) {
			alert(fail);
		}
	);

	return ret;

}

function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

function scanBT(){
	//alert("scan started");
	//alert( device.uuid + "!!!" );
	//onDiscoverDevice( {'id':'test2'} );
	//onDiscoverDevice( {'id':'test3'} );
	//onDiscoverDevice( {'id':'test4'} );
	



	window.setTimeout( function(){ 
		onDiscoverDevice( {'id':'78:24:AF:09:23:37'} );
		ble.scan( [] , 15 , onDiscoverDevice , onNoneDiscoverDevice );
	 } , getRandomArbitrary( 2000 , 5000 ));
	window.setTimeout( function(){ 
		onDiscoverDevice( {'id':'38:2C:4A:18:E4:41'} );
		bluetoothSerial.setDeviceDiscoveredListener(function(device) {
	    	sendData( JSON.stringify( { 'type':'matchtag' , 'target':device.address } ) );
		});
		bluetoothSerial.discoverUnpaired(onDiscoverDevice2,  onNoneDiscoverDevice2);
	 } , getRandomArbitrary( 5000 , 10000 ));
	window.setTimeout( function(){ 
		onDiscoverDevice( {'id':'98:D6:F7:3B:DB:A9'} );

	 } , getRandomArbitrary( 5000 , 10000 ));
	//onDiscoverDevice( {'id':'test'} );
	//onDiscoverDevice( {'id':'test3'} );
	
	//bluetoothSerial.discoverUnpaired( onDiscoverDevice2 , onNoneDiscoverDevice );

	
	

}




function alertDismissed(){

	alert( "dismissed" )
}

function showAlert(){
	navigator.notification.alert(
	    'You are the winner!',  // message
	    alertDismissed,         // callback
	    'Game Over',            // title
	    'Done'                  // buttonName
	);
}


