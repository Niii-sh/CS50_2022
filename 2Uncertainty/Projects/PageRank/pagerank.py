import os
import random
import re
import sys

# 就是Iterative Algorithm中的d
DAMPING = 0.85
# 代表抽样数量
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # ranks 为一个字典 有sample_pagerank 函数返回根据样本计算的 page对应其PageRank的字典
    # corpus即语料库课程已经提供给我们了
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.

    总的来说 就是直接帮助返回每个页面与其相连页面的关系 方便了很多操作
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    corpus: 为一个包含页面以及其即可到达页面的字典
    page: 为random surfer 当前访问的页面(也可以直接理解为 当前页面)
    damping_factor: d

    返回一个 字典包含 random surfer 在遍历 corpus中每个page时选择下一个page的概率
    所有返回的概率值的总和为1
    在 damping_factor 即d 概率的情况 random surfer 对于下一个遍历的页面的选择概率是相同的
    在 1-d 的情况 random surfer 在选择同一个corpus 下的page的概率时相同的
    当 当前页面没有其他可访问的链接时 返回 等概率下随机选择corpus的概率
    """

    """
    The transition_model should return a dictionary representing the probability distribution over 
    which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.
    这句话 直接摘自specification (这里是用了一个状语后置 given a corpus of pages ...这些应该提到前面 很容易引起误解)
    意思是说 再当前传入的corpus中的pages 和damping factor的情况下 返回一个表示random 下一个即将访问的page的概率分布
    """

    # 存放每一个 page 与之对应 概率 最后返回的也是这个东西
    distribution = dict()

    # 获取当前传入 语料(corpus)集合的page数量 之后遍历的时候要用到
    num_pages = len(corpus)

    # 获取当前page 链接到其他page的链接数
    num_links = len(corpus[page])

    # 接下来 就是用到那个公式 PR(p) = (1-d)/N + d ∑PR(i)/Numlinks(i)
    # 如果当前page 没有链接到其他页面 那么 ∑ 这一块就没有了 其概率就是前面(1-d)/N 这一部分
    if num_links == 0:
        page_prob = (1 - damping_factor) / num_pages
        # 建立当前page 可能到达该corpus 中所有page的概率分布 (没有链接 视为到达其他任何page的概率相同)
        for pageX in corpus:
            distribution[pageX] = page_prob
    else:
        page_prob = (1 - damping_factor) / num_links
        # 根据公式 有链接情况下的 PR(i) 就是这个
        link_prob = damping_factor / num_links + page_prob
        for pageX in corpus:
            # 如果该链接的页面 不在该corpus中 那么访问的概率为 1-d的那种情况 即page_prob
            if pageX not in corpus:
                distribution[pageX] = page_prob
            # 否则为PR(i) 的情况
            else:
                distribution[pageX] = page_prob

    if sum(distribution) is not 1:
        print("概率分布之和 非1")
        raise exit()

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    n: n为用于评估Page_Rank 的 sample 数量
    返回一个字典 包含每个corpus中的page所估计出的PageRank值 总和为1

    第一个sample 随机选择一个page 生成
    接下来每一个sample 则需要基于之前sample的 transition_model的基础上生成 (这个就是上面的transition_model函数产生)

    return an estimated PageRank for each page
    总的来说 sample_pagerank 返回当前corpus 中所有page的PageRank估计
    这个sample_rank 其实就是random surfer model 的完全实现
    """

    # 用于存储 sample的PageRank值
    sample_PR = dict()

    # 初始化所有page 的 pageRank值
    for page in corpus:
        sample_PR[page] = 0

    sample = None

    # corpus 存储的 page 与其对应的可以link到的page集合 遍历corpus.keys()就是遍历所有的page
    for page in corpus.keys():
        # First sample的情况 随机选择page 开始
        if sample is None:
            # 字典对应的值为集合 转化为list
            choices = list(corpus.keys())
            sample = random.choice(choices)
            # 第一个节点值 +1
            sample_PR[sample] = 1
        # 非First sample的情况 则基于前一个 sample的transition_model 选择page
        else:
            samples = transition_model(corpus, page, damping_factor)
            choices = list(samples)
            weights = list()
            for prob in choices:
                weights.append(prob)
            sample = random.choices(choices, weights).pop()
            sample_PR[sample] += 1

    # 遍历完成后 加所有值转为概率 即可
    for node in sample_PR:
        node = node / n

    # 这里小数点精确到5位 是因为specification 里面说最终返回的PageRank值的精确度应该在0.01之内
    if round(sum(sample_PR.values()), 5) is not 1:
        print("PageRank 概率之和非1")
        raise exit()

    return sample_PR


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    1.首先对每个page的rank  初始值1/N (N为所有corpus中page的总和)
    2.根据 PageRank formula 在已有的page rank基础上不断计算新的rank值(没有链接到其他page的 page视为链接所有的corpus 包括其本身所在corpus)
    3.重复2 知道PageRank改变值 小于0.01

    返回 一个字典包含每个corpus中的page的PageRank(通过) 其总和为1

    这个其实就是总的函数 需要完成对于所有sample的PageRank估计
    """
    # 最终返回的结果 每个page及其对应的PageRank
    iterate_PR = dict()

    num_pages = len(corpus)
    # 对每个page的pageRank 赋初始值
    for page in corpus:
        iterate_PR[page] = 1/num_pages

    # 最终要求其改变值不超过 0.01
    change = 1

    # 在现有的rank值基础上 不断通过公式 即sample_rank去计算新的rank值 直到其改变值小于0.01
    while change>=0.01:
        change = 0
        previous_state = iterate_PR.copy()
        for page in iterate_PR:
            sample_pagerank()

    raise NotImplementedError


if __name__ == "__main__":
    main()
