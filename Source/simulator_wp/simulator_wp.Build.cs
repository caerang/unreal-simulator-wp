using UnrealBuildTool;

public class simulator_wp : ModuleRules
{
	public simulator_wp(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "TurboLinkGrpc" });

		PrivateDependencyModuleNames.AddRange(new string[] {  });
	}
}
