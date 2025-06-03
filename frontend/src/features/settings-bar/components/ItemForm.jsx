import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import useItem from "../hooks/useItem";

const ItemForm = () => {
  const {
    action: { handleOnChange },
  } = useItem();

  return (
    <div className="hw-full flex items-center px-2">
      <Label className="w-1/4">Item Type:</Label>
      <Input
        className="w-3/4"
        placeholder={import.meta.env.VITE_TEST_ITEM}
        onChange={handleOnChange}
      />
    </div>
  );
};

export default ItemForm;
