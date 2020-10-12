# *_*coding:utf-8 *_*
from yq_worker.video_judgment.base import Base
import yq_worker.utils.tools as tools
from yq_worker.video_judgment.video_identification import *
class BaseJudge(Base):
    def is_video(self, p):
        try:
            # 央广网（中国广播网）
            if tools.judge_url_contained('cnr', p._url):
                p.set_website(cnr.CNR())
                result = p.is_video()
                if result:
                    return True

            # 中国网络电视台（CNTV）
            elif tools.judge_url_contained('cctv', p._url):
                p.set_website(cctv.CCTV())
                result = p.is_video()
                if result:
                    return True
            # 国际在线
            elif tools.judge_url_contained('cri', p._url):
                p.set_website(cri.CRI())
                result = p.is_video()
                if result:
                    return True
            # 人民网
            elif tools.judge_url_contained('people', p._url):
                p.set_website(people.People())
                result = p.is_video()
                if result:
                    return True
            # 新华网
            elif tools.judge_url_contained('xinhuanet', p._url):
                p.set_website(xinhua.XinHua())
                result = p.is_video()
                if result:
                    return True
            # 中国军网
            elif tools.judge_url_contained('81', p._url):
                p.set_website(military.Military())
                result = p.is_video()
                if result:
                    return True
            # 光明网
            elif tools.judge_url_contained('gmw', p._url):
                p.set_website(gmw.Gmw())
                result = p.is_video()
                if result:
                    return True
            # 中国经济网
            elif tools.judge_url_contained('ce', p._url):
                p.set_website(ce.Ce())
                result = p.is_video()
                if result:
                    return True
            # 中国日报网
            elif tools.judge_url_contained('chinadaily', p._url):
                pass
            # 人民政协网
            elif tools.judge_url_contained('rmzxb', p._url):
                pass
            # 环球网
            elif tools.judge_url_contained('huanqiu', p._url):
                p.set_website(huanqiu.HuanQiu())
                result = p.is_video()
                if result:
                    return True
            # 中国青年网
            elif tools.judge_url_contained('youth', p._url):
                p.set_website(youth.Youth())
                result = p.is_video()
                if result:
                    return True
            # 中青在线
            elif tools.judge_url_contained('cyol', p._url):
                p.set_website(cyol.Cyol())
                result = p.is_video()
                if result:
                    return True
            # 法制网
            elif tools.judge_url_contained('legaldaily', p._url):
                p.set_website(legaldaily.Legaldaily())
                result = p.is_video()
                if result:
                    return True
            # 中华女性网(暂未发现)
            elif tools.judge_url_contained('cnwomen', p._url):
               pass
            # 中国农业新闻网
            elif tools.judge_url_contained('farmer', p._url):
                p.set_website(farmer.Farmer())
                result = p.is_video()
                if result:
                    return True
            # 中国科技网
            elif tools.judge_url_contained('stdaily', p._url):
                p.set_website(stdaily.Stdaily())
                result = p.is_video()
                if result:
                    return True
            # 海外网
            elif tools.judge_url_contained('haiwainet', p._url):
                p.set_website(haiwainet.HaiWai())
                result = p.is_video()
                if result:
                    return True
            # 中工网(网站迁移http://www.workercn.cn/)
            # 视频少
            elif tools.judge_url_contained('workercn', p._url):
                pass
            # 党建网
            elif tools.judge_url_contained('dangjian', p._url):
                p.set_website(dangjian.DangJian())
                result = p.is_video()
                if result:
                    return True
            # 中国网
            elif tools.judge_url_contained('china', p._url):
                p.set_website(china.China())
                result = p.is_video()
                if result:
                    return True
            # 中新网（中国新闻网）
            elif tools.judge_url_contained('chinanews', p._url):
                p.set_website(chinanews.ChinaNews())
                result = p.is_video()
                if result:
                    return True
            # 虎嗅网(视频暂未发现)
            elif tools.judge_url_contained('huxiu', p._url):
                pass
            # 未来网
            elif tools.judge_url_contained('k618', p._url):
                p.set_website(weilai.WeiLai())
                result = p.is_video()
                if result:
                    return True
            # 北京时间(新闻数据和视频都不在源码中)
            elif tools.judge_url_contained('brtn', p._url):
                pass
            # 驱动中国
            elif tools.judge_url_contained('qudong', p._url):
                p.set_website(qudong.QuDong())
                result = p.is_video()
                if result:
                    return True
            # 东海网
            elif tools.judge_url_contained('dhtv', p._url):
                p.set_website(dhtv.Dhtv())
                result = p.is_video()
                if result:
                    return True
            # 比特网(暂未找到视频)
            elif tools.judge_url_contained('chinabyte', p._url):
                pass
            # 每经网(暂未找到视频)
            elif tools.judge_url_contained('nbd', p._url):
                pass
            # 中国文明网
            elif tools.judge_url_contained('wenming', p._url):
                p.set_website(wenming.WenMing())
                result = p.is_video()
                if result:
                    return True
            # 凤凰网
            elif tools.judge_url_contained('ifeng', p._url):
                p.set_website(fenghuang.Ifeng())
                result = p.is_video()
                if result:
                    return True
            # 新浪
            elif tools.judge_url_contained('sina', p._url):
                p.set_website(sina.Sina())
                result = p.is_video()
                if result:
                    return True
            # 搜狐
            elif tools.judge_url_contained('sohu', p._url):
                p.set_website(souhu.SouHu())
                result = p.is_video()
                if result:
                    return True
            # 网易网
            elif tools.judge_url_contained('163', p._url):
                p.set_website(wangyi.WangYi())
                result = p.is_video()
                if result:
                    return True
            # 百度新闻
            elif tools.judge_url_contained('baidu', p._url):
                pass
            # 猫扑
            elif tools.judge_url_contained('mop', p._url):
                pass

            # 澎湃网
            elif tools.judge_url_contained('thepaper', p._url):
                p.set_website(thepaper.Thepaper())
                result = p.is_video()
                if result:
                    return True
            # 腾讯网
            elif tools.judge_url_contained('qq', p._url):
                p.set_website(qq.QQ())
                result = p.is_video()
                if result:
                    return True
            # 中国新闻出版广电网
            elif tools.judge_url_contained("chinaxwcb", p._url):
                pass
            # 国家广播电视总局
            elif tools.judge_url_contained("nrta", p._url):
                pass
            # 东方网
            elif tools.judge_url_contained("eastday", p._url):
                p.set_website(eastday.EastDay())
                result = p.is_video()
                if result:
                    return True

            elif tools.judge_url_contained("cm3721", p._url):
                pass
            # 上观网
            elif tools.judge_url_contained("shobserver", p._url):
                pass
            # 新京报网
            elif tools.judge_url_contained("bjnews", p._url):
                p.set_website(bjnews.BjNews())
                result = p.is_video()
                if result:
                    return True
            else:
                return False

        except Exception:
            return False
