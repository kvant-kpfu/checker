from generator import *
from string import ascii_lowercase

inter = NodeInterpreter()

len_t = GenerateStableInt()
gen_t = GenerateStableString()
add_t = Add()
add_enter1 = AddEnter()

len_p = GenerateStableInt()
sub_t = Subtract()
gen_p = GenerateStableString()
add_p = Add()
add_enter2 = AddEnter()

gen_range = Range()
inc_t = Sum()
to_list = List()
shuffle = Shuffle()
add_range = Add()

############################

len_t.inputs["start"].connect(1)
len_t.inputs["end"].connect(200000)
len_t.outputs["result"].connect(gen_t.inputs["length"])

gen_t.inputs["allowed"].connect(ascii_lowercase)
gen_t.outputs["result"].connect(add_t.inputs["val"])

add_t.inputs["order_input"].connect(inter.start)
add_t.outputs["order_output"].connect(add_enter1.inputs["order_input"])

add_enter1.outputs["order_output"].connect(add_p.inputs["order_input"])

len_p.inputs["start"].connect(1)
sub_t.inputs["input1"].connect(len_t.outputs["result"])
sub_t.inputs["input2"].connect(1)
len_p.inputs["end"].connect(sub_t.outputs["result"])

gen_p.inputs["length"].connect(len_p.outputs["result"])
gen_p.inputs["allowed"].connect(ascii_lowercase)

add_p.inputs["val"].connect(gen_p.outputs["result"])
add_p.outputs["order_output"].connect(add_enter2.inputs["order_input"])

add_enter2.outputs["order_output"].connect(add_range.inputs["order_input"])

gen_range.inputs["start"].connect(1)
inc_t.inputs["input1"].connect(len_t.outputs["result"])
inc_t.inputs["input2"].connect(1)
gen_range.inputs["end"].connect(inc_t.outputs["result"])

to_list.inputs["input1"].connect(gen_range.outputs["range"])
shuffle.inputs["obj"].connect(to_list.outputs["result"])

add_range.inputs["val"].connect(shuffle.outputs["result"])
add_range.outputs["order_output"].connect(inter.end)

inter.execute()
print(Result().res)
