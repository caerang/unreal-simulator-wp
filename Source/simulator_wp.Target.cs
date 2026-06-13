using UnrealBuildTool;
using System.Collections.Generic;

public class simulator_wpTarget : TargetRules
{
	public simulator_wpTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V6;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		CppStandard = CppStandardVersion.Cpp20;
		ExtraModuleNames.Add("simulator_wp");
	}
}
