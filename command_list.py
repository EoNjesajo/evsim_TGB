class Command_list():  # 문자열을 명령어로
    # 문자열을 해석하여 명령어 리스트를 만들어 이동시킨다.
    def __init__(self):
        self.cm_list = list()

        self.rblk_cm = ''
        self.lblk_cm = ''
        self.fblk_cm = ''
        self.bblk_cm = ''

    def R(self):
        self.cm_list.append('R')

    def L(self):
        self.cm_list.append('L')

    def F(self):
        self.cm_list.append('F')

    def B(self):
        self.cm_list.append('B')

    def turn(self, blk, cm): # blk가 막혀있다면 cm으로 간다 설정
        if blk == 'R':
            self.rblk_cm = cm
        elif blk == 'L':
            self.lblk_cm = cm
        elif blk == 'F':
            self.fblk_cm = cm
        elif blk == 'B':
            self.bblk_cm = cm

    def get_blk(self, blk): # blk 막혀있을 때 설정해둔 cm 불러옴
        if blk == 'R':
            return self.rblk_cm
        elif blk == 'L':
            return self.lblk_cm
        elif blk == 'F':
            return self.fblk_cm
        elif blk == 'B':
            return self.bblk_cm

    def get_command(self):  # 만들어진 명령어 리스트를 반환한다.
        return self.cm_list