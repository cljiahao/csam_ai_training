import React, { useState } from "react";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { PiGauge } from "react-icons/pi";

import NavBar from "../../containers/common/NavBar";
import Menu from "../../containers/Menu/Menu";

const Settings = () => {
  const [menu, setMenu] = useState(false);

  const openMenu = async () => {
    setMenu(!menu);
  };

  const button_info = {
    Train: {
      icon: <LiaChalkboardTeacherSolid />,
      onClick: () => (window.location.href = "/"),
    },
    Evaluate: {
      icon: <PiGauge />,
      onClick: () => (window.location.href = "/"),
    },
  };
  return (
    <main className="flex h-screen w-screen bg-amber-100">
      <section className="w-full">test</section>
      <aside className="relative w-[60%] border-l-2 border-slate-400">
        <NavBar openMenu={openMenu} button_info={button_info} />
        <Menu openMenu={openMenu} menu={menu} />
      </aside>
    </main>
  );
};

export default Settings;
