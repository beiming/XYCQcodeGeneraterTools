import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.io.File;
import java.io.InputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import javax.xml.parsers.*;

import org.w3c.dom.*;

public class CodeGenerater
{
	//xml config
	private String SrcDirAttributeName = "SrcDir";
	private String ObjEventXmlName = "ObjEvent";

	private String UnPackFunctionName = "UnPackFunctionName";
	private String UpackClassPrefix = "UpackClassPrefix";
	private String UpackClassFunc = "UpackClassFunc";
	private String SendPackFunctionName = "SendPackFunctionName";
	private String SendPackClassPrefix = "SendPackClassPrefix";
	private String SendPackClassFunc = "SendPackClassFunc";

	private final Map<String,String> ReplaceFunctionName = new HashMap<String,String>();
	private final Map<String,String> ReplaceClassPrefix = new HashMap<String,String>();
	private final Map<String,String> ReplaceClassFunc = new HashMap<String,String>();

	//now event
	private String ObjEvent = "";
	private String NowFlag = "";
	private final String SendFlag = "send";
	private final String UnpackFlag = "unpack";

	//folder path
	private String SrcDir = "test";
	private String YxEventFileName = "Global\\YXEvent.as";
	private final Map<String,String> CommunicationFileName = new HashMap<String,String>();
	private final Map<String,String> OutPutDir = new HashMap<String,String>();
	private final Map<String,String> TemplateFileName = new HashMap<String,String>();
	private String configXMLFileName;


	//function match flag
	private final Map<String,String> CommunicationPreifx = new HashMap<String,String>();
	private final Map<String,String> CommunicationEventFlag = new HashMap<String,String>();
	private final Map<String,String> CommunicationEventFlagEnd = new HashMap<String,String>();
	private final String FunctionStatment = ".*function +";

	private final String EventMessageFlag = "#";
	private final String LeftBracket = "{";
	private final String RightBracket = "}";
	private final String LeftAnnotation = "/*";
	private final String RightAnnotation = "*/";

	//template match
	private final String NewClassNameFlag = "$Classname$";
	private final Map<String,String> NewFuncNameFlag =  new HashMap<String,String>();
	
	public CodeGenerater()
	{
		String path = this.getClass().getClassLoader().getResource("").getPath().substring(1);
		
		configXMLFileName = path + "config.xml";
		
		CommunicationFileName.put(UnpackFlag, "Global\\YXUnpacking.as");
		CommunicationFileName.put(SendFlag,  "Global\\YXPackSend.as");
		OutPutDir.put(UnpackFlag, "Global\\SocketUnpack");
		OutPutDir.put(SendFlag, "Global\\SocketSendpack");
		TemplateFileName.put(UnpackFlag, path+ "unPackTemplate.as");
		TemplateFileName.put(SendFlag, path+ "sendPackTemplate.as");
		
		CommunicationPreifx.put(UnpackFlag, "messageFunctionArray[YXEvent.EventStringSplite(YXEvent.");
		CommunicationPreifx.put(SendFlag, "YXAPI.dispatcher.addEventListener(YXEvent.");
		CommunicationEventFlag.put(UnpackFlag, "=");
		CommunicationEventFlag.put(SendFlag, ",");
		CommunicationEventFlagEnd.put(UnpackFlag, ";");
		CommunicationEventFlagEnd.put(SendFlag, ")");
		NewFuncNameFlag.put(UnpackFlag, "$unpack$");
		NewFuncNameFlag.put(SendFlag, "$send$");
		try
		{
			if(init())
			{
				String messageId = analyzeEventInfo();
				String funcName = analyzeFunctionInfo(UnpackFlag);
				if(funcName.length() == 0)
				{
					funcName = analyzeFunctionInfo(SendFlag);
				}
				if(messageId.length() > 0 && funcName.length() > 0)
				{
					System.out.printf("Find message Id: %s\nFind function name: %s\n", messageId, funcName);
					changeMessageFunction(ReplaceClassPrefix.get(NowFlag)+messageId, funcName);
				}
				else
				{
					System.out.printf("Error message Id: %s\nError function name: %s\n", messageId, funcName);
				}
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
	
	private void initVariable()
	{
		YxEventFileName = SrcDir + YxEventFileName;
		CommunicationFileName.put(UnpackFlag, SrcDir + CommunicationFileName.get(UnpackFlag));
		CommunicationFileName.put(SendFlag, SrcDir + CommunicationFileName.get(SendFlag));

		OutPutDir.put(UnpackFlag, SrcDir + OutPutDir.get(UnpackFlag) + File.separator);
		OutPutDir.put(SendFlag, SrcDir + OutPutDir.get(SendFlag) + File.separator);

		ReplaceFunctionName.put(UnpackFlag, UnPackFunctionName);
		ReplaceFunctionName.put(SendFlag, SendPackFunctionName);

		ReplaceClassPrefix.put(UnpackFlag, UpackClassPrefix);
		ReplaceClassPrefix.put(SendFlag, SendPackClassPrefix);

		ReplaceClassFunc.put(UnpackFlag, UpackClassFunc);
		ReplaceClassFunc.put(SendFlag, SendPackClassFunc);
		//System.out.println(OutPutDir.get(UnpackFlag));
	}
	
	public Boolean init() throws Exception
	{
		InputStream input = this.getClass().getClassLoader().getResourceAsStream("config.xml");
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document document = builder.parse(input);
		Element element = document.getDocumentElement();

		SrcDir = element.getAttribute(SrcDirAttributeName);
		if(SrcDir.length() == 0)
		{
			System.out.printf("%s is empty\n", SrcDirAttributeName);
			return false;
		}
		else
		{
			char endChar = SrcDir.charAt(SrcDir.length() - 1);
			if(endChar != '\\' &&  endChar != '/')
			{
				SrcDir += File.separator;
			}
			File dirname = new File(SrcDir);
			if(dirname.isDirectory())
			{
				UnPackFunctionName = element.getAttribute(UnPackFunctionName);
				UpackClassPrefix = element.getAttribute(UpackClassPrefix);
				UpackClassFunc = element.getAttribute(UpackClassFunc);
				SendPackFunctionName = element.getAttribute(SendPackFunctionName);
				SendPackClassPrefix = element.getAttribute(SendPackClassPrefix);
				SendPackClassFunc = element.getAttribute(SendPackClassFunc);

				NodeList node = element.getElementsByTagName(ObjEventXmlName);
				for (int i = 0; i < node.getLength(); i++)
				{
					Element bookElement = (Element) node.item(i);
					ObjEvent = bookElement.getTextContent();
					break;
				}
				if(ObjEvent.length() == 0)
				{
					System.out.printf("%s is empty\n", ObjEventXmlName);
					return false;
				}
				else
				{
					initVariable();
					return true;
				}
			}
			else
			{
				System.out.printf("No such Folder:\n%s\n", SrcDir);
				return false;
			}
		}
	}
	
	private String analyzeEventInfo() throws Exception
	{
		String resultStr = "";
		File file = new File(YxEventFileName);
		BufferedReader reader = new BufferedReader(new FileReader(file));
		String lineStr = reader.readLine();
		while (lineStr != null) 
		{
			if(lineStr.contains(ObjEvent))
			{
				resultStr = lineStr.trim();
				break;
			}
			lineStr = reader.readLine();
		}
		reader.close();
		if(resultStr.length() > 0)
		{
			int flagIndex = resultStr.lastIndexOf(EventMessageFlag) + 1;
			resultStr = resultStr.substring(flagIndex, resultStr.length() -2);
		}
		return resultStr;
	}
	
	private String analyzeFunctionInfo(String pNowFlag) throws Exception
	{
		String resultStr = "";
		NowFlag = pNowFlag;
		
		String nowUnpackMessage = CommunicationPreifx.get(NowFlag) + ObjEvent;
		File file = new File(CommunicationFileName.get(NowFlag));
		BufferedReader reader = new BufferedReader(new FileReader(file));
		String lineStr = reader.readLine();
		while (lineStr != null) 
		{
			if(lineStr.contains(nowUnpackMessage))
			{
				resultStr = lineStr.trim();
				break;
			}
			lineStr = reader.readLine();
		}
		reader.close();
		if(resultStr.length() > 0)
		{
			int flagStart = resultStr.lastIndexOf(CommunicationEventFlag.get(NowFlag)) + 1;
			int flagEnd = resultStr.lastIndexOf(CommunicationEventFlagEnd.get(NowFlag));
			resultStr = resultStr.substring(flagStart, flagEnd).trim();
		}
		return resultStr;
	}
	
	private void changeMessageFunction() throws Exception
	{
		File file = new File(CommunicationFileName.get(NowFlag));
		BufferedReader reader = new BufferedReader(new FileReader(file));
		Vector allLines = new Vector();
		String lineStr = reader.readLine();
		while (lineStr != null) 
		{
			allLines.add(lineStr);
			lineStr = reader.readLine();
		}
		reader.close();
		String nowUnpackMessage = CommunicationPreifx.get(NowFlag) + ObjEvent;
		int arrLen = allLines.size();
		//change function name
		int nameIndex = -1;
		for(int index = 0; index < arrLen; index++)
		{
			if((String)allLines.get(index).indexOf(nowUnpackMessage) != -1)
			{
				nameIndex = index;
				tempStr = (String)allLines.get(index).split(CommunicationEventFlag.get(NowFlag));
				tempStr[1] = tempStr[1].replace(funcName, className + ReplaceClassFunc.get(NowFlag));
				allLines[index] = tempStr[0] + CommunicationEventFlag.get(NowFlag) + tempStr[1];
				break;
			}
		}
		if(nameIndex == -1)
		{
			//return
		}
	}
	
	public static void main(String arg[])
	{
		CodeGenerater c=new CodeGenerater();
	}
}