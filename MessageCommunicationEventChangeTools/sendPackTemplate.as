package Global.SocketUnpack
{
	import ClassData.ChatData;
	import ClassData.JingjiAIData;
	import ClassData.Props.PropsBase;
	import ClassData.PropsBatchData;
	import ClassData.RoleData;
	
	import Enum.ChatEnum;
	import Enum.JingjiEnum;
	
	import Global.SocketSendpack.S16511;
	import Global.SocketSendpack.S8899;
	import Global.SocketSendpack.S9000;
	import Global.events.YXEventSocketSend;
	
	import com.adobe.crypto.MD5;
	
	import flash.geom.Point;
	import flash.utils.ByteArray;
    
	
	public class $Classname$ extends Sbase
	{
		private static var instance:$Classname$;
		public function $Classname$()
		{
			throwError(instance);
		}
		
		public static function getInstance():$Classname$
		{
			if (instance == null)
			{
				instance = new $Classname$;
			}
			return instance;
		}

$send$
	}
}
