import DoBotArm as Dbt
import time

class PickPlace:
    def __init__(self):
        self.z = 50
        self.item_Height1 = 10
        self.item_Height2 = -40
        self.offsett = 25
        self.offsett2 = 20
        self.offsett3 = 50
        self.ctrlDobot = None

    def Homing(self, homeX, homeY, homeZ):
        self.ctrlDobot = Dbt.DoBotArm("COM5", homeX, homeY, homeZ)

    def Conveyor(self, timer):
        self.ctrlDobot.SetConveyor(enabled=True, speed=10000)
        time.sleep(timer)
        self.ctrlDobot.SetConveyor(enabled=False, speed=-10000)

    def Loading(self, pixel_x, pixel_y, homeX, scalar1, num_items):
        mm_values_x = [x * scalar1 for x in pixel_x]
        mm_values_y = [-y * scalar1 for y in pixel_y]
        print('mm values for X coordinates are:', mm_values_x)
        print('mm values for Y coordinates are:', mm_values_y)

        for i in range(num_items):
            item_x = homeX - mm_values_x[i] - self.offsett2
            item_y = mm_values_y[i] + self.offsett3
            self.move_and_place(item_x, item_y, self.item_Height2)

            place_x = 200
            place_y = (i - num_items // 2) * 50
            self.move_and_place(place_x, place_y, self.item_Height1, suction=False)

        # Conveyor belt to left
        self.Conveyor(5)

    def Unloading(self, pixel_x, pixel_y, homeX, scalar2, num_items):
        mm_values_x = [x * scalar2 for x in pixel_x]
        mm_values_y = [-y * scalar2 for y in pixel_y]
        print('mm values for X coordinates are:', mm_values_x)
        print('mm values for Y coordinates are:', mm_values_y)

        for i in range(num_items):
            item_x = homeX - mm_values_x[i] - self.offsett2
            item_y = mm_values_y[i] + self.offsett
            self.move_and_place(item_x, item_y, self.item_Height1)

            place_x = 200 - (i - num_items // 2) * 50
            place_y = -200
            self.move_and_place(place_x, place_y, self.item_Height2, suction=False)

    def move_and_place(self, x, y, z, suction=True):
        self.ctrlDobot.moveArmXYZ(x, y, self.z, wait=True)
        self.ctrlDobot.moveArmXYZ(x, y, z, wait=True)
        if suction:
            self.ctrlDobot.toggleSuction(True)
        self.ctrlDobot.moveArmXYZ(x, y, self.z, wait=True)
        if not suction:
            self.ctrlDobot.toggleSuction(False)

if __name__ == "__main__":
    pick_place = PickPlace()
    pick_place.Homing(0, 0, 0)  # Replace with your desired home coordinates

    pixel_x = [10, 20, 30]  # Replace with your pixel coordinates
    pixel_y = [15, 25, 35]  # Replace with your pixel coordinates
    scalar1 = 1.0  # Replace with your scalar values
    num_items = len(pixel_x)

    pick_place.Loading(pixel_x, pixel_y, 100, scalar1, num_items)
    pick_place.Unloading(pixel_x, pixel_y, 100, scalar1, num_items)
