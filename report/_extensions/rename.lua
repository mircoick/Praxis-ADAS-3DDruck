function Header(el)
  local text = pandoc.utils.stringify(el)
  if el.level == 1 and (text == "List Of Acronyms" or text == "List of Acronyms") then
    el.content = {pandoc.Str("Abkürzungsverzeichnis")}
    el.classes:insert("unnumbered")
    return el
  end
end