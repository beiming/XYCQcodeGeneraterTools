import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.InputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;
import java.io.FileOutputStream;
import java.io.FileInputStream;
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
	
	private void changeMessageFunction(String className, String funcName) throws Exception
	{
		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(CommunicationFileName.get(NowFlag)), "UTF-8"));
		Vector<String> allLines = new Vector<String>();
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
		int index = 0;
		for(; index < arrLen; index++)
		{
			if(allLines.get(index).indexOf(nowUnpackMessage) != -1)
			{
				nameIndex = index;
				String tempStr[] = allLines.get(index).split(CommunicationEventFlag.get(NowFlag));
				tempStr[1] = tempStr[1].replace(funcName, className + ReplaceClassFunc.get(NowFlag));
				allLines.set(index, tempStr[0] + CommunicationEventFlag.get(NowFlag) + tempStr[1]);
				//System.out.printf("Debug :\n%s\n", allLines.get(index));
				break;
			}
		}
		if(nameIndex == -1)
		{
			return;
		}
		//delete original function statement
		int statement[] = findFuncStatment(allLines, funcName, index);
		if(statement[0] == -1)
		{
			System.out.printf("can\'t find the function declaration statement:\n%s", funcName);
			return;
		}
		ArrayList<String> funcStatement = new ArrayList();//allLines.subList(statement[0], statement[1] + 1);
		for(index = statement[0]; index < statement[1] + 1; index++)
		{
			funcStatement.add(allLines.get(index));
			allLines.set(index, "CodeGeneraterDeleted");
		}
		
		BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(CommunicationFileName.get(NowFlag)), "UTF-8"));
		for(index = 0; index < arrLen; index++)
		{
			String str = allLines.get(index);
			if(!str.equals("CodeGeneraterDeleted"))
			{
				writer.write(str, 0, str.length());
				writer.newLine();
			}
			writer.flush();
		}
		writer.close();
		System.out.printf("The Original unpack function had replaced with: %s\nand function: %s had removed\n", className + UpackClassFunc, funcName);
		creatClassFile(className, funcStatement);
	}
	
	private int[] findFuncStatment(Vector<String> lis, String funcName, int startIndex)
	{
		int result[] = {-1,-1};
		int funcDeclarationIndex = -1;
		int funcDeclarationStartIndex = -1;
		int funcDeclarationEndIndex = -1;
		int arrLen = lis.size();
		String pattern = FunctionStatment + funcName + ".*";
		for(int index = startIndex; index < arrLen; index++)
		{
			if(lis.get(index).matches(pattern))
			{
				lis.set(index ,lis.get(index).replace(funcName, ReplaceFunctionName.get(NowFlag)));
				if(lis.get(index).contains("private"))
				{
					lis.set(index, lis.get(index).replace("private", "public"));
				}
				else if(lis.get(index).contains("protected"))
				{
					lis.set(index, lis.get(index).replace("protected", "public"));
				}
				funcDeclarationIndex = index;
				break;
			}
		}
		if(funcDeclarationIndex == -1)
		{
			return result;
		}
		
		//find the first left bracket line index {
		int bracketMatch = -1;
		int leftBracketIndex = -1;
		for(int index = funcDeclarationIndex; index < arrLen; index++)
		{
			if(lis.get(index).contains(LeftBracket))
			{
				bracketMatch = 1;
				leftBracketIndex = index + 1;
				break;
			}
		}
		if(leftBracketIndex == -1)
		{
			return result;
		}
		
		//match brackets, find the function statement{}
		for(int index = leftBracketIndex; index < arrLen; index++)
		{
			if(lis.get(index).contains(LeftBracket))
			{
				 bracketMatch ++;
			}
			if(lis.get(index).contains(RightBracket))
			{
				 bracketMatch --;
			}
			if(bracketMatch == 0)
			{
				funcDeclarationEndIndex = index ;
				break;
			}
		}
		if(funcDeclarationEndIndex == -1)
		{
			return result;
		}
		
		//find the last function end }
		for(int index = funcDeclarationIndex; index > -1; index--)
		{
			if(lis.get(index).contains(RightBracket))
			{
				funcDeclarationStartIndex = index + 1;
				break;
			}
		}
		if(funcDeclarationIndex - funcDeclarationStartIndex > 30)
		{
			return result;
		}

		//find this function annotation area
		for(int index = funcDeclarationStartIndex; index < funcDeclarationIndex; index++)
		{
			if(lis.get(index).contains(LeftAnnotation))
			{
				funcDeclarationStartIndex = index;
				break;
			}
		}
		if(funcDeclarationIndex - funcDeclarationStartIndex > 30)
		{
			return result;
		}
		if(funcDeclarationEndIndex - funcDeclarationStartIndex < 1)
		{
			return result;
		}
		result[0] = funcDeclarationStartIndex;
		result[1] = funcDeclarationEndIndex;
		return result;
	}
	
	private void creatClassFile(String className, ArrayList<String> lis) throws Exception
	{
		String newClassFileName =  OutPutDir.get(NowFlag) + className + ".as";
		File newClassFile = new File(newClassFileName);
		if(newClassFile.exists())
		{
			System.out.printf("File already exists:\n%s", newClassFileName);
			return;
		}
		newClassFile.createNewFile();
		InputStreamReader reader = new InputStreamReader(new FileInputStream(new File(TemplateFileName.get(NowFlag))), "UTF-8");
		OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(newClassFile), "UTF-8");
		int temp = -1;
		while((temp = reader.read()) != -1)
		{
			writer.write((char)temp);
		}
		reader.close();
		writer.close();
		
		BufferedReader changeReader = new BufferedReader(new InputStreamReader(new FileInputStream(newClassFile), "UTF-8"));
		Vector<String> allLines = new Vector<String>();
		String lineStr = changeReader.readLine();
		while (lineStr != null) 
		{
			allLines.add(lineStr);
			lineStr = changeReader.readLine();
		}
		changeReader.close();
		int arrLen = allLines.size();
		int index = 0;
		for(index = 0; index < arrLen; index++)
		{
			if(allLines.get(index).contains(NewClassNameFlag))
			{
				allLines.set(index, allLines.get(index).replace(NewClassNameFlag, className));
			}
			else if(allLines.get(index).contains(NewFuncNameFlag.get(NowFlag)))
			{
				String funcStr = "";
				for(int i = 0; i < lis.size(); i++)
				{
					funcStr += lis.get(i) + "\r\n";
				}
				allLines.set(index, allLines.get(index).replace(NewFuncNameFlag.get(NowFlag), funcStr));
			}
		}
		
		BufferedWriter changeWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(newClassFile), "UTF-8"));
		for(index = 0; index < arrLen; index++)
		{
			String str = allLines.get(index);
			
			changeWriter.write(str, 0, str.length());
			changeWriter.newLine();
			changeWriter.flush();
		}
		changeWriter.close();
		System.out.printf("Creat Class:\n%s", newClassFileName);		
	}
	
	public static void main(String arg[])
	{
		CodeGenerater c=new CodeGenerater();
	}
}