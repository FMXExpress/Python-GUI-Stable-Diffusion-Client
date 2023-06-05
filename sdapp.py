from delphifmx import *
import replicate
import urllib.request
import hashlib
import os
os.environ["REPLICATE_API_TOKEN"] = ""

class StableDiffusionForm(Form):

    def __init__(self, owner):
        self.stylemanager = StyleManager(self)
        self.stylemanager.SetStyleFromFile("Air.style")

        self.SetProps(Caption="Stable Diffusion + Replicate API", OnShow=self.__form_show, OnClose=self.__form_close)

        self.layout_top = Layout(self)
        self.layout_top.SetProps(Parent=self, Align="Top", Height="50", Margins = Bounds(RectF(3, 3, 3, 3)))

        self.prompt_label = Label(self)
        self.prompt_label.SetProps(Parent=self.layout_top, Align="Left", Text="Prompt:", Position=Position(PointF(20, 20)), Margins = Bounds(RectF(3, 3, 3, 3)))

        self.prompt_edit = Edit(self)
        self.prompt_edit.SetProps(Parent=self.layout_top, Align="Client", Text="portrait photo headshot by mucha, sharp focus, elegant, render, octane, detailed, award winning photography, masterpiece, rim lit", Position=Position(PointF(80, 18)), Width=200, Margins = Bounds(RectF(3, 3, 3, 3)))

        self.generate_button = Button(self)
        self.generate_button.SetProps(Parent=self.layout_top, Align = "Right", Text="Generate", Position=Position(PointF(290, 18)), Width=80, OnClick=self.__button_click, Margins = Bounds(RectF(3, 3, 3, 3)))

        self.image_control = ImageControl(self)
        self.image_control.SetProps(Parent=self, Align="Client", Position=Position(PointF(20, 60)), Width=350, Height=350, Margins = Bounds(RectF(3, 3, 3, 3)))

    def __form_show(self, sender):
        self.SetProps(Width=640, Height=480)

    def __form_close(self, sender, action):
        action = "caFree"

    def __button_click(self, sender):
        prompt = self.prompt_edit.text
        global replicate
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": prompt, "negative_prompt": "canvas frame, cartoon, 3d, ((disfigured)), ((bad art)), ((deformed)),((extra limbs)),((close up)),((b&w)), wierd colors, blurry,  (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, video game, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render ENSD: 31337,"}
        )
        image_url = output[0]
        file_name = './' + hashlib.md5(image_url.encode()).hexdigest() + '.jpg'
        urllib.request.urlretrieve(image_url, file_name)
        self.image_control.LoadFromFile(file_name)

def main():
    Application.Initialize()
    Application.Title = "Stable Diffusion + Replicate API"
    Application.MainForm = StableDiffusionForm(Application)
    Application.MainForm.Show()
    Application.Run()
    Application.MainForm.Destroy()

if __name__ == '__main__':
    main()