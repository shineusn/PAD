import numpy as np

class Simple_Assoc(object):

  """ Simple way of associate picks by finding org_time clusters
  """
  def __init__(self, 
               ot_dev    = 2.5, 
               assoc_num = 4):
    
    self.ot_dev    = ot_dev
    self.assoc_num = assoc_num


  def pick2event(self, picks):
    event_picks = []
    num_picks = len(picks)

    # assoc each cluster
    for _ in range(num_picks):
        # calc neighbor num
        ots = picks['org_t0']
        num_nbr = np.zeros(len(ots))
        for i, oti in enumerate(ots):
            is_nbr = abs(ots-oti) < self.ot_dev
            num_nbr[i] = sum(is_nbr.astype(float))
        if np.amax(num_nbr) < self.assoc_num: break
        oti = ots[np.argmax(num_nbr)]
        is_nbr = abs(ots-oti) < self.ot_dev
        event_pick = picks[is_nbr]
        picks = picks[~is_nbr]
        event_picks.append(event_pick)

    print('associated {} events'.format(len(event_picks)))
    return event_picks


  def write(self, event_picks, out_pha):
    """ write event_picks into phase file
    """
    for event_pick in event_picks:
      num_sta = len(event_pick)
      org_t0  = event_pick['org_t0'][num_sta//2]
      out_pha.write('{},{}\n'.format(org_t0, num_sta))
      for pick in event_pick:
        net   = pick['network']
        sta   = pick['station']
        p_arr = pick['p_arr']
        s_arr = pick['s_arr']
        s_amp = pick['s_amp']
        p_snr = pick['p_snr']
        s_snr = pick['s_snr']
        out_pha.write('{},{},{},{},{:.1f},{:.1f},{:.1f}\n'\
                    .format(net, sta, p_arr, s_arr, s_amp, p_snr, s_snr))
    return
