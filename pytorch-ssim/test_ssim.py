import pytorch_ssim
import torch
from torch.autograd import Variable
from torch import optim
import cv2
import numpy as np
import os

g_basic_path = '/home/lhm/aibee_workspace/neck_test/src/neck_data/0603-test/'
min_s_score = 0.95

f_out = open('./0603-test_result_all.txt', 'w')
f_s = open('./0603-test_result_big.txt', 'w')
f_out.write('#file_name, index, ssim, lxy, cxy, sxy\n')
f_s.write('#file_name, index, sxy. score = ' + str(min_s_score) + '\n')

#f = open('./fileName.txt', 'r')
#lines = f.read().split('\n')
lines = os.listdir(g_basic_path)
print('get ', len(lines), ' files!')
#print(lines)
last_line = lines[0]
for current_line in lines: 
    img1_path = g_basic_path + last_line
    img2_path = g_basic_path + current_line

    for i in range(0, 6):
        print(img1_path + '/test-' + str(i) + '.jpg')
        npImg1 = cv2.imread(img1_path + '/test-' + str(i) + '.jpg')
        npImg2 = cv2.imread(img2_path + '/test-' + str(i) + '.jpg')

        npImg1 = cv2.resize(npImg1, (2080, 2080))
        npImg2 = cv2.resize(npImg2, (2080,2080))
        #cv2.imwrite('a.jpg', npImg1)
        #cv2.imwrite('b.jpg', npImg2)
        '''
        cv2.namedWindow('lena',cv2.WINDOW_NORMAL)
        cv2.imshow("lena", npImg1)
        cv2.waitKey()
        cv2.imshow("lena", npImg2)
        cv2.waitKey()
        '''

        img1 = torch.from_numpy(np.rollaxis(npImg1, 2)).float().unsqueeze(0)/255.0
        img2 = torch.from_numpy(np.rollaxis(npImg2, 2)).float().unsqueeze(0)/255.0
        #print(img1.size())
        #print(img2.size())
        if torch.cuda.is_available():
            img1 = img1.cuda()
            img2 = img2.cuda()

        img1 = Variable( img1,  requires_grad=False)
        img2 = Variable( img2,  requires_grad=False)

        # Functional: pytorch_ssim.ssim(img1, img2, window_size = 11, size_average = True)
        ssim_value = pytorch_ssim.ssim(img1, img2, window_size = 5)
        print("Initial ssim:", ssim_value)
        ssim_map = ssim_value[0].item()
        l_map = ssim_value[1].item()
        c_map = ssim_value[2].item()
        s_map = ssim_value[3].item()
        #print(l_map.item())
        f_out.write(str(current_line)+','+str(i)+','+str(ssim_map)+','+str(l_map)+','+str(c_map)+','+str(s_map)+'\n')
        if(s_map < min_s_score):
            f_s.write(str(current_line)+','+str(i)+','+str(s_map)+'\n')

f_out.close()
f_s.close()
#f.close()

'''
# Module: pytorch_ssim.SSIM(window_size = 11, size_average = True)
ssim_loss = pytorch_ssim.SSIM()

optimizer = optim.Adam([img2], lr=0.01)

while ssim_value < 0.95:
    optimizer.zero_grad()
    ssim_out = -ssim_loss(img1, img2)
    ssim_value = - ssim_out.data
    print(ssim_value)
    ssim_out.backward()
    optimizer.step()
'''
