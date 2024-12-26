import { FaHome } from "react-icons/fa";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";

// Information for different sections or pages with descriptions
const navigation_info = [
  {
    name: "Home",
    url: "/",
    title: "Home Page",
    description: "Home Page",
    icon: FaHome,
  },
  {
    name: "Example1",
    url: "/example1",
    title: "Example - 1",
    description: "Lead to Page Example 1.",
    icon: MdOutlineMoveToInbox,
  },
  {
    name: "Example2",
    url: "/example2",
    title: "Example - 2",
    description: "Lead to Page Example 2.",
    icon: LiaNetworkWiredSolid,
  },
  {
    name: "Example3",
    url: "/example3",
    title: "Example - 3",
    description: "Lead to Page Example 3.",
    icon: IoMdSettings,
  },
];

export { navigation_info };
