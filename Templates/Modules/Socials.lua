-- cache image files associated to a type
local data = mw.loadData('Module:Socials/data') or {}
local format = require "Module:Format"

---@class Socials
---@field ICON_SIZE number
local p = {
    ICON_SIZE = 25,

    TEMPLATES = {
        ICON = {
            DEFAULT = "[[{icon}|{iconSize}px|class={class}]]",
            WITH_LINK = "[[{icon}|link={link} |{iconSize}px|class={class}]]",
            WITH_PAGE = "[[{icon}|{iconSize}px|class={class}]]",
        },
        NO_TEXT = {
            DEFAULT = "{text}",
            WITH_LINK = "[{link} {text}]",
            WITH_PAGE = "[[{page}]]",
        },
        TEXT = {
            DEFAULT = "{text}",
            WITH_LINK = "[{link} {text}]",
            WITH_PAGE = "[[{page}|{text}]]",
        },
    },
}

---Retrieve the icon from provided type, or return `default`.
---@TODO: improve feedback for provided type not existing
---@param t string
---@return table
p._get_icon_link = function(t, page)
    t = t ~= "" and t
        or page and "pzwiki" -- no type provided, but page is provided, use pzwiki icon
        or "default" -- no icon nor type provided

    return data[t]
        or data["default"] -- provided type doesn't exists
end

p._format_param = function(param)
    local s = mw.text.trim(tostring(param or ""))
    if s == "" then return nil end
    return s
end



p.list_types_doc = function(frame)
    local out = {
        string.format("*[[%s|25px]] <code>%s</code> %s", data["default"].file, "default", data["default"].doc_comment or ""),
    }

    -- get every icon types and sort them by key
    local keys = {}
    for k,v in pairs(data) do repeat
        if k == "default" then break end
        table.insert(keys, k)
    until true end -- the repeat until here is used to allow a continue statement
    table.sort(keys, function(a,b) return a:lower() < b:lower() end)

    for _,k in ipairs(keys) do
        local v = data[k]
        table.insert(out, string.format("*[[%s|25px|class=%s]] <code>%s</code> %s", v.file, v.class or "", k, v.doc_comment or ""))
    end
    return table.concat(out, "\n")
end

---Main function to be called from wikitext.
---@param frame frame
p.socials = function(frame)
    local args = frame.args
    local link = p._format_param(args["link"])
    local page = p._format_param(args["page"])

    -- retrieve icon
    local _icon_arg = p._format_param(args["icon"]) -- use custom one
    local icon_link = _icon_arg and {file=_icon_arg}
        or p._get_icon_link(args["type"], page) -- use predefined one

    -- retrieve the text, remove spaces at the start and end
    local text = p._format_param(args["1"]) or "link"

    local params = {
        icon = icon_link.file,
        class = icon_link.class or "",
        iconSize = tostring(p.ICON_SIZE),
        text = text,
    }
    params.link = link
    params.page = page

    local template_icon_id = link and "WITH_LINK"
        or page and "WITH_PAGE"
        or "DEFAULT"
    local template_text_id = link and "WITH_LINK"
        or page and "WITH_PAGE"
        or "DEFAULT"

    local template_icon = p.TEMPLATES.ICON[template_icon_id]
    local template_text = text == "link" and p.TEMPLATES.NO_TEXT[template_text_id]
        or p.TEMPLATES.TEXT[template_text_id]

    local out_icon = format._format_string(template_icon, params)
    local out_text = format._format_string(template_text, params)

    return out_icon .. " " .. out_text
end

return p
