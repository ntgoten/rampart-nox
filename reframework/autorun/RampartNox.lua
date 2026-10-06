-- RampartNox: Rampart Breaker (male, TopsStyle Tops_266) with its shirt and sleeves in dark purple.
-- Only the material colours change: the pak adds two skins (tops_968_wb_m_00 / tops_968_am_m_00 = copies of
-- Rampart's material files with purple recolour / tint values); this script registers them in the skin catalogs
-- under our own IDs (Content Editor method, needs DD2MethodLibrary) and points Rampart's shirt (Wb) and sleeves
-- (AmSub) at them. Meshes, gloves, belts and physics stay vanilla.
-- Script Generated UI > "Rampart Nox": status, restore.
local PFB = "AppSystem/CharaEdit/ch000/Parts/tops/"
local SKINS = {
    { cat = "_TopsWbSkinCatalog", id = 968001, path = PFB .. "wb/skin/tops_968_wb_m_00.pfb", field = "_WbSkinID" },
    { cat = "_TopsAmSkinCatalog", id = 968002, path = PFB .. "am/skin/tops_968_am_m_00.pfb", field = "_AmSubSkinID" },
}
local status, applied, tries, original = "waiting for the game", false, 0, nil

local function enum_value(t, f) local td = sdk.find_type_definition(t); local fd = td and td:get_field(f); return fd and fd:get_data(nil) end

local function rampart(cem)
    local male = cem:get_field("_TopsDB"):call("get_Item", enum_value("app.Gender", "Male"))
    return male:call("get_Item", enum_value("app.TopsStyle", "Tops_266"))
end

local function register(cem, s)
    local cat = cem:get_field(s.cat)
    if not cat or cat:call("get_Count") == 0 then error(s.cat .. " not loaded yet") end
    local have = cat:call("ContainsKey", s.id) and cat:call("get_Item", s.id)
    if have and have:call("get_ResourcePath") == s.path then return end
    if type(MethodLibrary) == "nil" then error("DD2MethodLibrary plugin missing") end
    local ctrl = sdk.create_instance("app.PrefabController"):add_ref()
    local pfb = sdk.create_instance("via.Prefab"):add_ref()
    MethodLibrary.prefab_set_path(pfb, sdk.create_managed_string(s.path))
    ctrl:set_field("_Item", pfb)
    if cat:call("ContainsKey", s.id) then cat:call("set_Item", s.id, ctrl) else cat:call("Add", s.id, ctrl) end
end

local function refresh_player()
    local p = sdk.get_managed_singleton("app.CharacterManager")["<ManualPlayer>k__BackingField"]
    if p then p:call("get_HumanPartSwapper"):call("swapTops") end
end

local function apply()
    local cem = sdk.get_managed_singleton("app.CharacterEditManager")
    if not cem then error("CharacterEditManager not ready") end
    local item = rampart(cem)
    if not item then error("Tops_266 swap item not found") end
    for _, s in ipairs(SKINS) do register(cem, s) end
    if not original then
        original = {}
        for _, s in ipairs(SKINS) do
            local v = item:get_field(s.field)
            original[s.field] = (v == s.id) and nil or v      -- don't record our own value after a script reload
        end
    end
    for _, s in ipairs(SKINS) do item:set_field(s.field, s.id) end
    pcall(refresh_player)
end

local function restore()
    local item = rampart(sdk.get_managed_singleton("app.CharacterEditManager"))
    for f, v in pairs(original or {}) do item:set_field(f, v) end
    pcall(refresh_player)
end

re.on_frame(function()
    if applied then return end
    tries = tries + 1
    if tries % 60 ~= 1 then return end
    local ok, e = pcall(apply)
    if ok then applied = true; status = "applied"
    else status = "waiting: " .. tostring(e); if tries > 60 * 600 then applied = true; status = "gave up: " .. tostring(e) end end
end)

re.on_draw_ui(function()
    if not imgui.tree_node("Rampart Nox") then return end
    imgui.text(status)
    if imgui.button("Apply again") then local ok, e = pcall(apply); status = ok and "applied again" or ("error: " .. tostring(e)) end
    imgui.same_line()
    if imgui.button("Restore original colours") then local ok, e = pcall(restore); status = ok and "restored" or ("error: " .. tostring(e)) end
    imgui.tree_pop()
end)
