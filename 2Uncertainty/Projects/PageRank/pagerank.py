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
        page_prob = (1-damping_factor)/num_pages
        # 建立当前page 可能到达该corpus 中所有page的概率分布 (没有链接 视为到达其他任何page的概率相同)
        for pageX in corpus:
            distribution[pageX] = page_prob
    else:
        page_prob = (1-damping_factor)/num_links
        # 根据公式 有链接情况下的 PR(i) 就是这个
        link_prob = damping_factor/num_links + page_prob
        for pageX in corpus:
            # 如果该链接的页面 不在该corpus中 那么访问的概率为 1-d的那种情况 即page_prob
            if pageX not in corpus:
                distribution[pageX] = page_prob
            # 否则为PR(i) 的情况
            else:
                distribution[pageX] = page_prob

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

    """



    raise NotImplementedError


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
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
