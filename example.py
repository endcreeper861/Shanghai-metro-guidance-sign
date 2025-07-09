from sign import EXIT_COLOR, Arrow, BilingualText, ExitSign, NumberLine, Sign

# 生成简单的导向标识
sign = Sign(512, 128)
sign.add_element(NumberLine(108, 3))
sign.add_element(Arrow(108, direction="right"))
sign.save("line_3_right.png")

# 多线路换乘标识
sign = Sign(512 + 128, 128)
sign.add_element(Arrow(108, direction="up"))
sign.add_element(NumberLine(108, [4, 6, 9]))
sign.save("century_avenue.png")

# 生成站台导向标识
sign = Sign(2048, 128)
sign.add_element(NumberLine(108, 1), "center")
sign.add_element(Arrow(108, direction="left"))
sign.add_element(BilingualText(108, "往富锦路", "To Fujing Road"))
sign.add_element(BilingualText(108, "往莘庄", "To Xinzhuang"), "right")
sign.add_element(Arrow(108, direction="right"), "right")
sign.save("platform_sign.png")

# 生成出口标识
sign = Sign(1024, 256)
sign.add_element(ExitSign(108, "1,5-22"), "center")
sign.add_element(Arrow(108, EXIT_COLOR, direction="up"), "center")
sign.save("exit_sign.png")

# 自定义导向标识牌的背景色
sign = Sign(1024, 256, "#026AA7", padding=64)
sign.add_element(BilingualText(128, "市域机场线", "Airport Link Line"), "center")
sign.add_element(Arrow(128, direction="down"), "center")
sign.save("airport_link_line.png")
