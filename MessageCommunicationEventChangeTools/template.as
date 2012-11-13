package Global.SocketUnpack
{
	import flash.utils.ByteArray;
	import ClassData.AccumulateGiftData;
	import ClassData.AchieveData;
	import ClassData.ActivitiesData;
	import ClassData.AstrolabePanelData;
	import ClassData.AwardData;
	import ClassData.BuffIcoData;
	import ClassData.ChallengeBossData;
	import ClassData.ChallengeChapterData;
	import ClassData.ChallengeSaodangAwardData;
	import ClassData.ChatData;
	import ClassData.DaFuWengData;
	import ClassData.DaFuWengSelectLevelData;
	import ClassData.DemonFurnaceData;
	import ClassData.DungeonAwardData;
	import ClassData.FormulaData;
	import ClassData.FormulaTypeData;
	import ClassData.HeartData;
	import ClassData.JingjiAIData;
	import ClassData.JingjiAwardData;
	import ClassData.JingjiChallengeData;
	import ClassData.JingjiHeroData;
	import ClassData.JingjiResultData;
	import ClassData.JingjiRevengeData;
	import ClassData.JingjiWinData;
	import ClassData.MailData;
	import ClassData.MainUiButtonMangerData;
	import ClassData.MainUiEquipRefineryLineData;
	import ClassData.MapData;
	import ClassData.MapDataChange;
	import ClassData.MoneyShopData;
	import ClassData.NpcData;
	import ClassData.OpenActivityData;
	import ClassData.PetData;
	import ClassData.PetDemonPotData;
	import ClassData.PetEvolutionData;
	import ClassData.Props.EquipData;
	import ClassData.Props.GemData;
	import ClassData.Props.ItemData;
	import ClassData.Props.MaterialsData;
	import ClassData.Props.PropsBase;
	import ClassData.PropsBatchData;
	import ClassData.RankingData;
	import ClassData.RoleData;
	import ClassData.SchoolData;
	import ClassData.SchoolPositionData;
	import ClassData.SchoolRoleData;
	import ClassData.SchoolSkillResearchData;
	import ClassData.SchoolSkillStudyData;
	import ClassData.ServerInfo;
	import ClassData.ShortcutSKillData;
	import ClassData.SkillData;
	import ClassData.SpeakData;
	import ClassData.SpeakSelectData;
	import ClassData.TaskData;
	import ClassData.TaskPropAlertData;
	import ClassData.TaskTokenData;
	import ClassData.TeamData;
	import ClassData.TitleData;
	import ClassData.VIPInfoData;
	
	import Control.WindowManager;
	import Control.person.Fighter;
	import Control.person.Role;
	import Control.round.BuffDesc;
	import Control.round.BuffInfo;
	import Control.round.CatchInfo;
	import Control.round.DamageInfo;
	import Control.round.FleeInfo;
	import Control.round.HurtInfo;
	import Control.round.RoundInfo;
	import Control.round.SpeakInfo;
	import Control.round.SummonInfo;
	
	import Enum.BuffEnum;
	import Enum.ChatEnum;
	import Enum.EffectEnum;
	import Enum.GlobalEnum;
	import Enum.JingjiEnum;
	import Enum.PacksEnum;
	import Enum.PetAttribEnum;
	import Enum.PetEnum;
	import Enum.PropsBindingRulesEnum;
	import Enum.PropsEnum;
	import Enum.PropsQualityEnum;
	import Enum.RankingEnum;
	import Enum.RoleAttribEnum;
	import Enum.RoleEnum;
	import Enum.SkillEnum;
	import Enum.TaskEnum;
	
	import flash.geom.Point;
	import flash.utils.ByteArray;
	import flash.utils.getTimer;
	import Global.YXTools;
	import Global.YXAPI;
	import Global.YXCommonFunction;
	import Global.YXConfig;
	import Global.YXDictionary;
	import Global.YXConfig;
	import Global.YXApplicationDomainClass;
	import Global.YXCommonBitmapData;
	import Global.YXEvent;
	import Global.YXFilter;
	import Global.YXLoaderGameInit;
	import Global.YXLoaderGameModule;
	import Global.YXLoaderManger;
	import Global.YXLoopManager;
    
	
	public class $Classname$ extends UBase
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

$unpack$
	}
}
