import gym
import torch
import cv2 as cv
import numpy as np
import multiprocessing as mp
import copy
from enum import Enum
import pkg_resources

def __grad2bog__(val):
    return val / 180 * np.pi

def __bog2grad__(val):
    return val / np.pi * 180

class StateSpace(Enum):
    CARTESIAN = 0
    EULER = 1
    CARTESIAN_AND_EULER = 2
    CARTESIAN_DIFFERENCE = 3

class Environment():
    def __init__(self, max_steps:int, device = 'cpu'):
        self.max_steps = max_steps
        self.steps = 0
        self.state_dim = None
        self.action_dim = None
        self.state = None
        self.device = device
        self.done = False

        self.reward_top = 1.
        self.reward_loose = -1.
        self.reward_default = 0.

    def reset(self):
        raise NotImplementedError()

    def step(self):
        raise NotImplementedError()
    
    def render(self, display = True, show_debug_info = False):
        raise NotImplementedError()
    
class GymCartPoleV1(Environment):
    def __init__(
            self,
            max_steps:int = 400,
            device = 'cpu'
        ):
        super(GymCartPoleV1, self).__init__(device)
        self.max_steps = max_steps
        self.__env__ = gym.make('CartPole-v1', render_mode='rgb_array')
        self.state_dim = self.__env__.observation_space.shape[0]
        self.action_dim = self.__env__.action_space.n

    def reset(self) -> tuple[torch.Tensor, float, bool]:
        self.steps = 0
        state, _ = self.__env__.reset()
        state = torch.tensor(state).unsqueeze(0).to(self.device)
        self.state = state
        self.done = False
        return state, 0., self.done
    
    def step(self, action:int) -> tuple[torch.Tensor, float, bool]:
        state, reward, self.done, _, _ = self.__env__.step(action)

        self.steps += 1

        if self.done:
            reward = -1.
        if self.steps >= self.max_steps:
            reward = -1.
            self.done = True

        self.state = torch.tensor(state).unsqueeze(0).to(self.device)
        return self.state, reward, self.done
    
    def render(self, display = True, show_debug_info = False):
        img = self.__env__.render()

        if show_debug_info:
            
            
            cart_x = self.state[0, 0].item() / 2.4#4.8
            pole_x = cart_x + self.state[0, 2].item() / 2.4

            top_y = 171
            base_y = 298

            l = top_y - base_y

            c_x = img.shape[1] // 2

            cart_px = int(np.round(c_x + cart_x * img.shape[1] // 2))
            cart_py = base_y


            arrow_len = 30
            # arrow cart velocity
            cart_velocity = self.state[0, 1].item()
            cart_velo_px = int(np.round(cart_px + arrow_len * cart_velocity))
            cart_velo_py = cart_py
            img = cv.arrowedLine(img, (cart_px, cart_py), (cart_velo_px, cart_velo_py), color=(0, 0, 255), thickness=2)

            # arrow pole velocity
            pole_px = int(np.round(c_x + pole_x * img.shape[1] // 2))
            dx = pole_px - cart_px
            theta = np.arccos(dx / l)
            pole_py = int(np.round(cart_py + np.sin(theta) * l))

            pole_velocity = self.state[0, 3].item()
            pole_velo_px = int(np.round(pole_px + np.sin(theta) * arrow_len * pole_velocity))
            pole_velo_py = int(np.round(pole_py - np.cos(theta) * arrow_len * pole_velocity))
            img = cv.arrowedLine(img, (pole_px, pole_py), (pole_velo_px, pole_velo_py), color=(0, 0, 255), thickness=2)

            # text
            img = cv.putText(img, f'Cart Poition: {self.state[0, 0]:0.4f}', (10, 20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))
            img = cv.putText(img, f'Cart Velocity: {self.state[0, 1]:0.4f}', (10, 40), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))
            img = cv.putText(img, f'Pole Position: {self.state[0, 2]:0.4f}', (10, 60), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))
            img = cv.putText(img, f'Pole Velocity: {self.state[0, 3]:0.4f}', (10, 80), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))
            img = cv.putText(img, f'Steps: {self.steps}', (10, 100), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))
            img = cv.putText(img, f'Theta: {theta / np.pi * 180:0.3f}', (10, 120), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0))

        if display:
            cv.imshow('CartPole-v1', img)
            cv.waitKey(30)
        return img

class Pendulum(Environment):
    def __init__(self, max_steps:int = 600, l = 1, m = 50., dt = 0.05, damping = 1e-3, device = 'cpu'):
        super(Pendulum, self).__init__(device)

        self.max_steps = max_steps
        self.dv = 50

        self.reward_top = 1.
        self.reward_default = 0.
        self.reward_loose = -10.

        self.action_dim = 2
        self.state_dim = 3

        self.l = l
        self.m = m
        self.g = 9.81
        
        self.dt = dt / 1000
        self.damping = damping

        self.factor_omega = 333

        self.reset()

    def reset(self, random = False, theta = 0):
        if random:
            self.px = (-1. + 2. * np.random.random()) * 0.25
            self.theta = np.random.random() * 2 * np.pi
            self.omega = 2 * (np.random.random() - 0.5) * 0.033
        else:
            self.px = 0.
            self.theta = 0. if theta is None else theta / 180 * np.pi
            self.omega = 0.
        self.steps = 0
        self.reward = 0.
        
        self.t = 0

        self.done = False
        self.state = torch.tensor([self.px, self.theta, self.omega * self.factor_omega], dtype=torch.float32).unsqueeze(0).to(self.device)
        return self.state, 0., self.done
        
    def sim_step(self):
        self.omega *= (1. - self.damping)

        a = np.sin(self.theta) * self.g

        self.omega += a * self.m * self.dt / self.l
        self.theta -= self.omega

        self.t += self.dt
        self.steps += 1
        pass

    def step(self, action:int):
        #dv = 50#100
        dx = 100

        domega = self.dv / self.l

        direction = -1 if action == 0 else 1

        self.px += dx * direction * self.dt

        self.omega += np.cos(self.theta) * domega * direction * self.dt

        self.sim_step()

        self.done = False

        reward_cos = -np.cos(self.theta) * self.reward_top
    
        if self.px < -0.5 or self.px > 0.5:
            self.done = True
            reward = self.reward_loose
        else:
            reward = reward_cos * self.reward_top

        if self.steps >= self.max_steps:
            self.done = True

        self.reward += reward
        self.state = torch.tensor([self.px, self.theta, self.omega * self.factor_omega], dtype=torch.float32).unsqueeze(0).to(self.device)
        
        return self.state, reward, self.done

    def render(self, display = True, show_debug_info = False):
        size = (500, 800, 3)
        img = np.full(size, 255, dtype=np.uint8)

        color_gray = (200, 200, 200)
        color_light_gray = (240, 240, 240)

        margin = 200
        
        w = (img.shape[1] - 2 * margin)
        h = (img.shape[0] - 2 * margin)
        r = int(np.round(0.05 * w))

        l = 0.8 * w

        p1x = img.shape[1] // 2 + int(np.round(self.px * w))
        p1y = img.shape[0] // 2
        p2x = p1x + int(np.round(np.sin(self.theta) * 0.5 * l))
        p2y = p1y + int(np.round(np.cos(self.theta) * 0.5 * l))

        img = cv.line(img, (0, img.shape[0] // 2), (img.shape[1], img.shape[0] // 2), color=color_gray, thickness=1)
        img = cv.line(img, (img.shape[1] // 2, img.shape[0] // 2 - 5), (img.shape[1] // 2, img.shape[0] // 2 + 5), color=color_gray, thickness=1)
        img = cv.rectangle(img, (0, 0), (margin, img.shape[0]), color=color_light_gray, thickness=-1)
        img = cv.rectangle(img, (img.shape[1] - margin, 0), (img.shape[1], img.shape[0]), color=color_light_gray, thickness=-1)

        cross_size = 5
        img = cv.line(img, (p1x - cross_size, p1y - cross_size), (p1x + cross_size, p1y + cross_size), color=(200,200,200), thickness=2)
        img = cv.line(img, (p1x + cross_size, p1y - cross_size), (p1x - cross_size, p1y + cross_size), color=(200,200,200), thickness=2)

        img = cv.line(img, (p1x, p1y), (p2x, p2y), color=(0,0,0), thickness=1)
        img = cv.circle(img, (p2x, p2y), radius=r, color=(0,0,0), thickness=-1)

        arrow1_x = p2x
        arrow1_y = p2y
        arrow2_x = arrow1_x + int(np.round(np.cos(self.theta + np.pi) * self.omega * 1000))
        arrow2_y = arrow1_y + int(np.round(np.sin(self.theta) * self.omega * 1000))
        img = cv.arrowedLine(img, (arrow1_x, arrow1_y), (arrow2_x, arrow2_y), color=(30, 30, 200), thickness=2)

        if show_debug_info:
            img = cv.putText(img, f'Cart Position: {self.px:0.2f}', (margin + 10, 20), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(60,60,60))
            img = cv.putText(img, f'Angular Velocity: {self.omega:0.2f}', (margin + 10, 40), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(60,60,60))
            img = cv.putText(img, f'Angle: {self.theta:0.2f}', (margin + 10, 60), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(60,60,60))
            img = cv.putText(img, f'Steps: {self.steps}', (margin + 10, 80), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(60,60,60))   
            img = cv.putText(img, f'Reward: {self.reward:0.2f}', (margin + 10, 100), cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(60,60,60))            

        if display:
            cv.imshow('CartPole', img)
            cv.waitKey(30)

        return img

class InvertedPendulum(Pendulum):
    def __init__(self, l = 1, m = 50., dt = 0.05, damping = 1e-3):
        super(InvertedPendulum, self).__init__(l, m, dt, damping)

    def step(self, action:int):
        state, reward, done = super(InvertedPendulum, self).step(action)
        if -np.cos(self.theta) < 0.8:
            self.done = True
            reward = self.reward_loose
        return state, reward, done
    
    def reset(self):
        super(InvertedPendulum, self).reset(random=False, theta=180)
        return self.state, 0., self.done

class Actor2D(Environment):
    def __init__(
            self,
            max_steps:int,
            dalpha:float = 0.01,
            target_radius:int = 0.15,
            state_space:StateSpace = StateSpace.CARTESIAN_AND_EULER,
            random_initialization:bool = False,
            device = 'cpu',
            adaptive_target_radius = True
        ):
        super(Actor2D, self).__init__(max_steps, device)
        self.l1 = 1.
        self.l2 = 1.1
        self.target_radius = target_radius
        self.max_target_radius = self.target_radius
        self.min_target_radius = 0.05
        self.state_space = state_space
        self.random_initialization = random_initialization
        self.adaptive_target_radius = adaptive_target_radius

        self.dalpha = dalpha

        if state_space == StateSpace.CARTESIAN_AND_EULER:
            self.state_dim = 8
        elif state_space == StateSpace.CARTESIAN_DIFFERENCE:
            self.state_dim = 4
        else:
            self.state_dim = 6
        self.action_dim = 4

        self.reward_top = 1.
        self.reward_default = 0.0
        self.reward_loose = -1.

        self.min_cos_alpha2 = 0.1

        self.alpha1_min = __grad2bog__(-0.)
        self.alpha1_max = __grad2bog__(150.)
        self.alpha2_min = __grad2bog__(-140.)
        self.alpha2_max = __grad2bog__(-30.)
        pass

        self.__init_joints__()
        self.blank_img = self.draw_working_area()

        self.final_rewards = []

    def __set_state__(self):
        j1x, j1y, j2x, j2y, j3x, j3y = self.__joint_poisitions__()
        dx, dy = j3x - self.target_x, j3y - self.target_y
        
        if self.state_space == StateSpace.CARTESIAN:
            self.state = torch.tensor([j3x, j3y, self.target_x, self.target_y, dx, dy], dtype=torch.float32).unsqueeze(0)
        elif self.state_space == StateSpace.EULER:
            self.state = torch.tensor([self.alpha1, self.alpha2, self.target_x, self.target_y, dx, dy], dtype=torch.float32).unsqueeze(0)
        elif self.state_space == StateSpace.CARTESIAN_AND_EULER:
            self.state = torch.tensor([self.alpha1, self.alpha2, j3x, j3y, self.target_x, self.target_y, dx, dy], dtype=torch.float32).unsqueeze(0)
        elif self.state_space == StateSpace.CARTESIAN_DIFFERENCE:
            self.state = torch.tensor([dx, dy], dtype=torch.float32).unsqueeze(0)

    def __init_joints__(self):
        while True:
            self.alpha1 = self.alpha1_min + np.random.random() * (self.alpha1_max - self.alpha1_min)
            self.alpha2 = self.alpha2_min + np.random.random() * (self.alpha2_max - self.alpha2_min)
            tool_x, tool_y = self.__euler_to_cartesian__(self.alpha1, self.alpha2)
            if tool_y > 0:
                break

    def __init_target__(self):
        while True:
            t_alpha1 = self.alpha1_min + np.random.random() * (self.alpha1_max - self.alpha1_min)
            t_alpha2 = self.alpha2_min + np.random.random() * (self.alpha2_max - self.alpha2_min)
            self.target_x, self.target_y = self.__euler_to_cartesian__(t_alpha1, t_alpha2)
            center_dist = np.sqrt(self.target_x**2 + self.target_y**2)
            if center_dist > (self.l1 + self.l2):
                continue
            # if center_dist + self.target_radius > (self.l1 + self.l2):
            #     continue
            break
            # if self.target_y > 0 + self.target_radius:
            #     break

    def __joint_poisitions__(self, alpha1 = None, alpha2 = None):
        alpha1 = self.alpha1 if alpha1 is None else alpha1
        alpha2 = self.alpha2 if alpha2 is None else alpha2
        j1x = 0.
        j1y = 0.
        j2x = j1x + np.cos(alpha1) * self.l1
        j2y = j1y + np.sin(alpha1) * self.l1
        j3x = j2x + np.cos(alpha1 + alpha2) * self.l2
        j3y = j2y + np.sin(alpha1 + alpha2) * self.l2
        return j1x, j1y, j2x, j2y, j3x, j3y

    def __euler_to_cartesian__(self, angle1, angle2):
        j2x = np.cos(angle1) * self.l1
        j2y = np.sin(angle1) * self.l1
        j3x = j2x + np.cos(angle1 + angle2) * self.l2
        j3y = j2y + np.sin(angle1 + angle2) * self.l2
        return j3x, j3y
    
    def __get_target_dist__(self):
        tool_x, tool_y = self.__euler_to_cartesian__(self.alpha1, self.alpha2)
        dx = tool_x - self.target_x
        dy = tool_y - self.target_y
        dist = np.sqrt(dx**2 + dy**2)
        return dist

    def reset(self):
        self.__init_joints__()
        if not self.random_initialization:
            self.alpha1 = __grad2bog__(90)
            self.alpha2 = __grad2bog__(-90)

        self.__init_target__()

        self.steps = 0
        self.reward = 0.
        self.last_dist_rel = 0.

        self.__set_state__()
        #self.state = torch.tensor([self.alpha1, self.alpha2, self.target_x, self.target_y], dtype=torch.float32).unsqueeze(0)

        return self.state, 0., False

    def step(self, action):
        # action    
        # 0: a1--
        # 1: a1++
        # 2: a2--
        # 3: a2++

        if action == 0:
            self.alpha1 -= self.dalpha
        elif action == 1:
            self.alpha1 += self.dalpha
        elif action == 2:
            self.alpha2 -= self.dalpha
        elif action == 3:
            self.alpha2 += self.dalpha
        else:
            raise Exception(f'Value {action} is not supported.')

        j3x, j3y = self.__euler_to_cartesian__(self.alpha1, self.alpha2)

        dist = np.sqrt(j3x**2 + j3y**2)
        dist_max = 2 * self.l1 + self.l1
        dist_rel = dist / dist_max

        self.steps += 1

        if self.target_reached():
            reward = self.reward_top
            done = True
        # elif np.abs(np.cos(0.5 * self.alpha2)) < self.min_cos_alpha2:
        #     reward = self.reward_loose
        #     done = True
        elif self.alpha1 < self.alpha1_min or self.alpha1 > self.alpha1_max or self.alpha2 < self.alpha2_min or self.alpha2 > self.alpha2_max:
            reward = self.reward_loose
            done = True
        # elif j3y < 0:
        #     reward = self.reward_loose
        #     done = True
        elif self.steps >= self.max_steps:
            done = True
            reward = self.reward_loose
        else:
            #reward = - dist_rel
            reward = self.reward_default# (self.last_dist_rel - dist) * self.reward_default
            done = False

        # if self.target_reached():
        #     done = True

        self.__set_state__()
        #self.state = torch.tensor([self.alpha1, self.alpha2, self.target_x, self.target_y], dtype=torch.float32).unsqueeze(0)

        self.reward += reward
        self.last_dist_rel = copy.copy(dist_rel)

        if done:
            self.final_rewards.append(reward)
            if len(self.final_rewards) >= 1000 and self. adaptive_target_radius:
                reward_avg = np.average(self.final_rewards[-1000:])
                self.target_radius = self.max_target_radius - (reward_avg + 1) / 2 * (self.max_target_radius - self.min_target_radius)

        return self.state, reward, done
        
    def target_reached(self):
        dist = self.__get_target_dist__()
        if dist <= self.target_radius:
            return True
        return False
        
    # working area
    def draw_working_area(self):
        img = np.ones((500, 500, 3), dtype=np.float32)
        margin_pixel = 50
        scale = (np.max([img.shape[0], img.shape[1]]) / 2 - margin_pixel) / (self.l1 + self.l2)
        color = (0.95, 0.95, 0.95)
        l2_px = int(np.round(self.l2 * scale))

        step = 0.005
        #np.arange()
        for alpha1 in np.arange(self.alpha1_min, self.alpha1_max, step=step):
            j1x, j1y, j2x, j2y, j3x, j3y = self.__joint_poisitions__(alpha1, None)
            clx = img.shape[1] // 2 + int(np.round(j2x * scale))
            cly = img.shape[0] // 2 - int(np.round(j2y * scale))
            #if alpha1 <= np.pi:
            img = cv.ellipse(img,
                                center=(clx, cly),
                                axes=(l2_px, l2_px), 
                                angle=__bog2grad__(-alpha1), 
                                startAngle=__bog2grad__(-self.alpha2_min), 
                                endAngle=__bog2grad__(-self.alpha2_max),
                                color=color,
                                thickness=1)
        return img

    def render(self, display = True, show_debug_info = False):
        img = self.blank_img.copy()# np.ones((500, 500, 3))

        j1x, j1y, j2x, j2y, j3x, j3y = self.__joint_poisitions__()

        margin_pixel = 50
        scale = (np.max([img.shape[0], img.shape[1]]) / 2 - margin_pixel) / (self.l1 + self.l2)

        p1x = img.shape[1] // 2 + int(np.round(j1x * scale))
        p1y = img.shape[0] // 2 - int(np.round(j1y * scale))

        p2x = img.shape[1] // 2 + int(np.round(j2x * scale))
        p2y = img.shape[0] // 2 - int(np.round(j2y * scale))

        p3x = img.shape[1] // 2 + int(np.round(j3x * scale))
        p3y = img.shape[0] // 2 - int(np.round(j3y * scale))

        tx = img.shape[1] // 2 + int(np.round(self.target_x * scale))
        ty = img.shape[0] // 2 - int(np.round(self.target_y * scale))

        joint_radius = 5
        link_thick = 8

        link_color = (20/255, 128/255, 245/255)
        joint_color = (0.4, 0.4, 0.4)

        # target
        r_t = int(np.round(scale * self.target_radius))

        dist = self.__get_target_dist__()
        dist_rel = dist / ((self.l1 + self.l2) * 2)

        target_color_red = (2*dist_rel-0.8)**3+1
        target_color_green = -(10 * dist_rel**2 - 1.)
        target_color_blue = 0.
        
        img = cv.circle(img, (tx, ty), radius=r_t, color=(target_color_blue, target_color_green, target_color_red), thickness=-1)
        img = cv.line(img, (p3x, p3y), (tx, ty), color=(target_color_blue, target_color_green, target_color_red), thickness=1)
        img = cv.putText(img, f'{dist:0.2f}', (p3x+(tx-p3x)//2, p3y+(ty-p3y)//2), color=(target_color_blue, target_color_green, target_color_red), fontScale=0.4, fontFace=cv.FONT_HERSHEY_SIMPLEX)

        # joints and limbs
        def add_overlay(img, overlay):
            overlay = cv.resize(overlay, (img.shape[0], img.shape[1]))
            mask = overlay[:, :, 3] == 255
            #mask = np.stack([mask, mask, mask], axis=2)
            img[:, :, 0][mask] = overlay[:, :, 0][mask] / 255
            img[:, :, 1][mask] = overlay[:, :, 1][mask] / 255
            img[:, :, 2][mask] = overlay[:, :, 2][mask] / 255
            return img
        
        def resize(img, scale):
            size_x, size_y = int(np.round(scale * img.shape[1])), int(np.round(scale * img.shape[0]))
            resized_img = cv.resize(img, (size_y, size_x))
            sx = img.shape[1] // 2 - resized_img.shape[1] // 2
            ex = sx + resized_img.shape[1]
            sy = img.shape[0] // 2 - resized_img.shape[0] // 2
            ey = sy + resized_img.shape[0]
            out_img = np.zeros(img.shape)
            out_img[sy:ey, sx:ex] = resized_img
            return out_img
        
        def shift(img, dx, dy):
            num_rows, num_cols = img.shape[:2]   

            translation_matrix = np.float32([[1,0,dx], [0,1,dy] ])   
            result = cv.warpAffine(img, translation_matrix, (num_cols, num_rows))
            return result
        
        def margin_to_target_size(img, target_size):
            result = np.zeros((target_size[0], target_size[1], img.shape[2]))
            sx = (target_size[1] - img.shape[1]) // 2
            ex = sx + img.shape[1]
            sy = (target_size[0] - img.shape[0]) // 2
            ey = sx + img.shape[0]
            result[sy:ey, sx:ex] = img
            return result
        
        def rotate_image(image, angle, cx, cy):
            image_center = (cx, cy)
            rot_mat = cv.getRotationMatrix2D(image_center, __bog2grad__(angle), 1.0)
            result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
            return result
        
        def load_image_resource(resource_name):
            #stream = pkg_resources.resource_stream('rsp', resource_name)
            fname = pkg_resources.resource_filename('rsp', resource_name)
            img = cv.imread(fname, cv.IMREAD_UNCHANGED)
            return img

            # img = np.array(Image.open(stream))
            # print(f'base.shape {img.shape}')
            # img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            # print(f'base.shape {img.shape}')
            # return img

        ol_scale = 0.49
        ox = 8
        oy = -46
        
        #base = cv.imread('data/image/robot-kuka-base.png', cv.IMREAD_UNCHANGED)
        base = load_image_resource('drl/environment/image/robot-kuka-base.png')
        

        base = resize(base, ol_scale)
        base = shift(base, ox, oy)
        base = margin_to_target_size(base, (img.shape[0], img.shape[1]))
        img = add_overlay(img, base)

        #link2 = cv.imread('data/image/robot-kuka-link2.png', cv.IMREAD_UNCHANGED)
        link2 = load_image_resource('drl/environment/image/robot-kuka-link2.png')
        link2 = resize(link2, ol_scale)
        l2_px = int(np.round(self.l2 * scale))
        link2 = shift(link2, p2x - l2_px - 138, p2y - 201)
        link2 = margin_to_target_size(link2, (img.shape[0], img.shape[1]))
        link2 = rotate_image(link2, self.alpha1 + self.alpha2 + 0.06*np.pi / 2, p2x, p2y)
        img = add_overlay(img, link2)

        #link1 = cv.imread('data/image/robot-kuka-link1.png', cv.IMREAD_UNCHANGED)
        link1 = load_image_resource('drl/environment/image/robot-kuka-link1.png')
        link1 = resize(link1, ol_scale)
        link1 = shift(link1, ox, oy)
        link1 = margin_to_target_size(link1, (img.shape[0], img.shape[1]))
        link1 = rotate_image(link1, self.alpha1 - np.pi / 2, 250, 250)
        img = add_overlay(img, link1)

        # img = cv.line(img, (p1x, p1y), (p2x, p2y), color=link_color, thickness=link_thick)
        # img = cv.line(img, (p2x, p2y), (p3x, p3y), color=link_color, thickness=link_thick)
        # img = cv.circle(img, (p1x, p1y), radius=joint_radius, color=joint_color, thickness=-1)
        # img = cv.circle(img, (p2x, p2y), radius=joint_radius, color=joint_color, thickness=-1)
        # img = cv.circle(img, (p3x, p3y), radius=joint_radius, color=joint_color, thickness=-1)

        # base
        #img = cv.line(img, (0, img.shape[0]//2), (img.shape[1], img.shape[0]//2), color=(0.5, 0.5, 0.5), thickness=1)

        if show_debug_info:
            img = cv.putText(img, f'Distance: {dist:0.2f}', (10, img.shape[0]-140), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Alpha1: {self.alpha1 / np.pi * 180:0.2f}', (10, img.shape[0]-120), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Alpha2: {self.alpha2 / np.pi * 180:0.2f}', (10, img.shape[0]-100), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Actor: [{j3x:0.2f}, {j3y:0.2f}]', (10, img.shape[0]-80), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Target: [{self.target_x:0.2f}, {self.target_y:0.2f}]', (10, img.shape[0]-60), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Steps: {self.steps}/{self.max_steps}', (10, img.shape[0]-40), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))
            img = cv.putText(img, f'Reward: {self.reward:0.4f}', (10, img.shape[0]-20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0., 0., 0.))

        if display:
            cv.imshow('Actor2D', img)
            cv.waitKey(1)

        return img

if __name__ == '__main__':
    #ENVIRONMENT = 'CartPole-v1'
    #ENVIRONMENT = 'Pendulum'
    #ENVIRONMENT = 'InvertedPendulum'
    ENVIRONMENT = 'Actor2D'

    #CONTROL_MODE = 'random'
    CONTROL_MODE = 'manual'

    if ENVIRONMENT == 'CartPole-v1':
        env = GymCartPoleV1()
    elif ENVIRONMENT == 'Pendulum':
        env = Pendulum()
    elif ENVIRONMENT == 'InvertedPendulum':
        env = InvertedPendulum()
    elif ENVIRONMENT == 'Actor2D':
        env = Actor2D(max_steps=100000)
    else:
        raise Exception(f'ENVIRONMENT {ENVIRONMENT} is not supported.')

    while True:
        state, reward, done = env.reset()
        env.render(display=True, show_debug_info=True)

        while not done:
            if CONTROL_MODE == 'random':
                action = np.random.randint(0, env.action_dim)
            elif CONTROL_MODE == 'manual':
                if ENVIRONMENT == 'Actor2D':
                    key = cv.waitKey()
                    if key == ord('1'):
                        action = 0
                    elif key == ord('2'):
                        action = 1
                    elif key == ord('3'):
                        action = 2
                    elif key == ord('4'):
                        action = 3
                    else:
                        action = -1
                else:
                    key = cv.waitKey()
                    if key == 2:    # arrow left
                        action = 0
                    elif key == 3:  # arrow right
                        action = 1
                    elif key == 0 and ENVIRONMENT == 'LineTrack':  # arrow top -> just for LineTrack environment
                        action = 2
                    else:
                        action = -1
            else:
                raise Exception(f'CONTROL_MODE {CONTROL_MODE} is not supported.')
            
            if action != -1:
                state, reward, done = env.step(action)

            env.render(display=True, show_debug_info=True)