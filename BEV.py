import carla
import numpy as np
import cv2
import time

def main():
    # === Connect to CARLA ===
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # === Spawn Ego Vehicle ===
    vehicle_bp = blueprint_library.filter('vehicle.*model3*')[0]
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)

    # === Attach Top-Down RGB Camera ===
    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute('image_size_x', '700')
    cam_bp.set_attribute('image_size_y', '700')
    cam_bp.set_attribute('fov', '90')
    
    cam_transform = carla.Transform(carla.Location(x=10, z=20), carla.Rotation(pitch=-90))
    camera = world.spawn_actor(cam_bp, cam_transform, attach_to=vehicle)

    # === Image Callback ===
    def process_image(image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((image.height, image.width, 4))[:, :, :3]
        array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        cv2.imshow("Bird's Eye View", array)
        cv2.waitKey(1)

    camera.listen(lambda image: process_image(image))

    # === Let It Run ===
    time.sleep(5)

    # === Cleanup ===
    camera.stop()
    vehicle.destroy()
    camera.destroy()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
