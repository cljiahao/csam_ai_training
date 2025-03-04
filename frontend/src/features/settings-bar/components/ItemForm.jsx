import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import useItem from "../hooks/useItem";

const ItemForm = () => {
  const {
    action: { handleOnChange },
  } = useItem();

  return (
    <div className="hw-full flex items-center px-4">
      <Label className="w-1/3">Item Type</Label>
      <Input
        className="w-2/3"
        placeholder="GCM32E106"
        onChange={handleOnChange}
      />
    </div>
  );
};

export default ItemForm;
