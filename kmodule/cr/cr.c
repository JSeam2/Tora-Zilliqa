#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/string.h>
#include <linux/uaccess.h>
#include <linux/smp.h>
#include <asm/uaccess.h>

MODULE_LICENSE("GPL");

static int __init module_oninit(void);
static void __exit module_onexit(void);
ssize_t proc_read_cr(struct file *file, char __user *buf, size_t size, loff_t *offset);

module_init(module_oninit);
module_exit(module_onexit);

struct file_operations proc_ops = {
    .owner = THIS_MODULE,
    .read = proc_read_cr
};

int read = 0;

static int __init module_oninit(void)
{
    if (!proc_create("cr", 0444, NULL, &proc_ops)) {
        printk(KERN_ERR "cr: failed to register proc entry\n");
        return -EINVAL;
    }

    printk(KERN_INFO "cr: successfully loaded\n");
    return 0;
}

static void __exit module_onexit(void)
{
    remove_proc_entry("cr", NULL);
    printk(KERN_INFO "cr: successfully unloaded\n");
}

void get_control_registers(void *buf)
{
    uint64_t cr0, cr2, cr3, cr4;
    char *tmp_buf;

    asm volatile("mov %%cr0, %%rax\nmov %%rax, %0" : "=m" (cr0) :: "ax");
    asm volatile("mov %%cr2, %%rax\nmov %%rax, %0" : "=m" (cr2) :: "ax");
    asm volatile("mov %%cr3, %%rax\nmov %%rax, %0" : "=m" (cr3) :: "ax");
    asm volatile("mov %%cr4, %%rax\nmov %%rax, %0" : "=m" (cr4) :: "ax");

    tmp_buf = kmalloc(200, GFP_KERNEL);

    if (!tmp_buf) {
        printk(KERN_ERR "cr: failed to allocate buffer\n");
        return;
    }

    sprintf(tmp_buf, "Control registers on cpu %u:\ncr0: %llx\ncr2: %llx\ncr3: %llx\ncr4: %llx\n",
        smp_processor_id(), cr0, cr2, cr3, cr4);
    strcat((char *)buf, tmp_buf);

    kfree(tmp_buf);
}

ssize_t proc_read_cr(struct file *file, char __user *buf, size_t size, loff_t *offset)
{
    int len;
    char *out_buf;

    if (read) {
        read = 0;
        return 0;
    }
    read = 1;

    out_buf = kmalloc(200 * num_online_cpus(), GFP_KERNEL);

    if (!out_buf) {
        printk(KERN_ERR "cr: failed to allocate buffer\n");
        return -1;
    }

    strcpy(out_buf, "");
    on_each_cpu(get_control_registers, out_buf, 1);

    len = strlen(out_buf);
    copy_to_user(buf, out_buf, len);

    kfree(out_buf);

    return (ssize_t)len;
}
