using UnrealBuildTool;
using System.Collections.Generic;

public class simulator_wpeditorTarget : TargetRules
{
	public simulator_wpeditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V6;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		CppStandard = CppStandardVersion.Cpp20;
		ExtraModuleNames.Add("simulator_wp");
	}
}
