import { Separator } from "@/components/ui/separator";
import BaseLayout from "@/components/layouts/BaseLayout";
import DescriptiveHeader from "@/components/static/descriptive-header";
import SettingsBar from "@/features/settings-bar/SettingsBar";
import SettingsFinder from "@/features/settings-finder/SettingsFinder";

const Settings = () => {
  return (
    <BaseLayout className="flex flex-col overflow-auto bg-yellow-100">
      <div className="flex py-2">
        <DescriptiveHeader
          className="w-2/3"
          title="CSAM Auto Settings Finder"
          description="Upload image to start finding its setting."
        />
        <Separator orientation="vertical" />
        <SettingsBar className="w-1/3" />
      </div>
      <div className="px-4">
        <Separator />
      </div>
      <div className="hw-full flex min-h-0 flex-1">
        <div className="h-full w-2/3">
          <SettingsFinder mode="Batch" />
        </div>
        <div className="h-full w-1/3">
          <SettingsFinder mode="Chip" />
        </div>
      </div>
    </BaseLayout>
  );
};

export default Settings;
