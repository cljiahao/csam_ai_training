import useItem from "../../../hooks/useItem";

const ItemSettings = () => {
  const {
    state: { item },
  } = useItem();

  return (
    <div className="hw-full flex-center">
      {item ? (
        <div>Settings for Image</div>
      ) : (
        <div>Item not found in Database</div>
      )}
    </div>
  );
};

export default ItemSettings;
