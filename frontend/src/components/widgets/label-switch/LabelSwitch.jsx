import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";

const LabelSwitch = ({
  className,
  labelClassName,
  label,
  checked,
  onCheckedChange,
}) => {
  return (
    <div className={cn("flex-center hw-full gap-6", className)}>
      <Switch id={label} checked={checked} onCheckedChange={onCheckedChange} />
      <Label htmlFor={label} className={cn("capitalize", labelClassName)}>
        {label}
      </Label>
    </div>
  );
};

export default LabelSwitch;
